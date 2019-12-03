from rest_framework import serializers
from updater.models import News

class NewsSerializer(serializers.ModelSerializer):
    """Django Rest Framework serializer for the News model"""
    #Field 'created' must be in iso-8601 format
    created = serializers.DateTimeField(format='iso-8601')
    class Meta:
        model = News
        fields = '__all__'
