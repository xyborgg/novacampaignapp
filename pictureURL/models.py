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

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["-date_created"]

class Analytics (models.Model):
    device = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=250)
    campaign_url = models.ForeignKey(Pictureurl, on_delete=models.CASCADE)
    timestamps = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.campaign_url