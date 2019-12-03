import requests
from bs4 import BeautifulSoup as BS
from django.test import TestCase
from updater.tasks import fetch_news
from hacker_news.settings import FETCH_URL, NUMBER_OF_NEWS_IN_PACKAGE

class TestUpdater(TestCase):
    def setUp(self):
        pass

    def test_fetching_news(self):
        """test method tries to fetch 56 news from url https://news.ycombinator.com/news and compares result in db via model News"""
        self.assertEquals(fetch_news(FETCH_URL, 56), 56)

    def test_posts_endpoint(self):
        """test method tries to request to the end-point /posts/ """
        r = requests.get('http://127.0.0.1:8000/posts')
        json = r.json()
        #json array must have length equal to parameter settings.NUMBER_OF_NEWS_IN_PACKAGE
        self.assertEquals(len(json), NUMBER_OF_NEWS_IN_PACKAGE)
        
        #json array must have length equal to GET-parameter limit 
        r = requests.get('http://127.0.0.1:8000/posts?offset=5&limit=10')
        json = r.json()
        self.assertEquals(len(json), 10)        
        
        #json dict must have keys: id, title, url, created
        s1 = set(list(json[0].keys()))
        s2 = set(['id', 'title', 'created','url'])
        self.assertEquals(s1.issubset(s2) and s2.issubset(s1), True)                
