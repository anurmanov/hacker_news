import logging
import re
import requests
from bs4 import BeautifulSoup as BS
from celery.schedules import crontab
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from updater.models import News
from hacker_news.celery import app
from hacker_news.settings import NUMBER_OF_NEWS_IN_PACKAGE, FETCH_FREQUENCY_IN_SECONDS, FETCH_URL

logger = logging.getLogger('news_model')

def get_package_of_rows(url):
    """Func fetchs all news from url via requests and bs4 modules"""
    try:
        r = requests.get(url)
        soup = BS(r.text, 'html.parser')
        rows = soup.find_all('tr', class_='athing')
    except:
        rows = None
    return rows

def write_news_to_db(news):
    """Func writes news to database and result is number of newly inserted items"""
    inserted_news = 0
    for row in news:
        cols = row.find_all('td')
        id = row.get('id')
        try:
            n = News.objects.get(id=id)
            n.title=cols[2].text
            n.url=cols[2].a.get('href')
            n.save(force_update=True)
        except ObjectDoesNotExist:
            n = News()
            n.id=id
            n.title=cols[2].text
            n.url=cols[2].a.get('href')
            n.save()
            inserted_news+=1
    return inserted_news

@app.task(bind = True, expires = 120, acks_late = True)
def fetch_news(self, fetch_url=FETCH_URL, number_of_news_in_package=NUMBER_OF_NEWS_IN_PACKAGE):
    """Celery task function is intended for fetching required number of the news from the url and writing them to the database"""
    inserted_news = 0
    url = fetch_url
    rows_for_processing = get_package_of_rows(url)
    if rows_for_processing:
        number_of_news_per_page = len(rows_for_processing)
        count_of_news_in_db = len(News.objects.all())
        #via count of the items in db and numberp of the news per page we calculate next page for fetching
        page = count_of_news_in_db // number_of_news_per_page + (1 if (count_of_news_in_db % number_of_news_per_page == 0) else 0)
        #slice operator : is used for get only required news from url
        inserted_news = write_news_to_db(rows_for_processing[:number_of_news_in_package])
        #cycle for fetching/writing required number of the news no more, no less
        while inserted_news < number_of_news_in_package:
            url = fetch_url + 'p=' + str(page)
            rows = get_package_of_rows(url)
            if rows:
                rows_for_processing = rows[:number_of_news_in_package - inserted_news]
                page+=1
            else:
                break
            inserted_news += write_news_to_db(rows_for_processing)
    #Task returns a number of the news inserted to the database
    return inserted_news

#Config dictionary for periodic Celery task
app.conf.beat_schedule = {
    'frequently-data-fetching': {
        'task': 'updater.tasks.fetch_news',
        'schedule': FETCH_FREQUENCY_IN_SECONDS
    },
}
