# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.
class Pictureurl(models.Model):
    auid = models.CharField(max_length=13, null=True)
    title = models.CharField(max_length=100)
    image_path = models.TextField()
    details = models.TextField(null=True)
    file_name = models.CharField(max_length=100)
    short_link = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    hyperlink = models.CharField(max_length=220, null=True )
    action = models.CharField(max_length=13, null=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["-date_created"]


class AnalyticsManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, Pictureurl):
            obj, created = self.get_or_create(instance=instance)
            obj.count =+ 1
            obj.save()
            return obj.count
        return None


class Analytics (models.Model):
    device = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=250)
    campaign_url = models.ForeignKey(Pictureurl, on_delete=models.CASCADE)
    timestamps = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    objects = AnalyticsManager()

    def __str__(self):
        return self.campaign_url


