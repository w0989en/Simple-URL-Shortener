from django.db import models
from django.utils import timezone


class ShortURL(models.Model):
    id = models.BigIntegerField()
    full_url = models.TextField(blank=True)
    short_url = models.CharField(max_length=200, primary_key=True)  # case sensitive
    remark = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)

