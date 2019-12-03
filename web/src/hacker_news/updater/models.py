from django.db import models

class News(models.Model):
    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'
    id = models.CharField(max_length=20, unique=True, blank=False, null=False, primary_key=True)
    title = models.CharField(max_length=500, blank=False, null=False)
    url = models.CharField(max_length=1000, blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
