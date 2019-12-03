import logging
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from .serializers import NewsSerializer
from hacker_news.settings import NUMBER_OF_NEWS_IN_PACKAGE, STRICT_MODE, MAX_LIMIT_OF_NEWS
from .models import News

logger = logging.getLogger('news_model')

class NewsListView(ListAPIView):
    """Django Rest Framework class view for the GET method to end-point /posts/"""
    serializer_class = NewsSerializer
    def get_queryset(self):
        offset = self.request.GET.get('offset', '0')
        order = self.request.GET.get('order', 'id').lower()
        limit = self.request.GET.get('limit', str(NUMBER_OF_NEWS_IN_PACKAGE))
        try:
            offset = int(offset, 10)
        except:
            logger.debug('GET paramater "offset" is not integer!')
            offset = 0
        else:
            if offset <= 0:
                logger.debug('GET paramater "offset" is not integer!')
                offset = 0
        
        if not (order in [f.name for f in News._meta.get_fields()]):
            logger.debug('There is no column "' + order + '" in the news fields!')
            order = 'id'
        try:
            limit = int(limit, 10)
        except:
            logger.debug('GET paramater "limit" is not integer!')
            limit = NUMBER_OF_NEWS_IN_PACKAGE
        else:
            if limit <= 0 or limit > MAX_LIMIT_OF_NEWS:
                logger.debug('GET paramater "limit" must be in the range from 1 to ' + str(MAX_LIMIT_OF_NEWS) + '!')
                limit = MAX_LIMIT_OF_NEWS
        return News.objects.all().order_by(order)[int(offset): int(offset + limit)]
