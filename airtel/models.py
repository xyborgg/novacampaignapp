from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Create your models here.


class Download(models.Model):
    msisdn = models.CharField(max_length=13, null=True)
    status = models.BooleanField(default=False)
    device = models.CharField(max_length=50, null=True)
    influencer = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.msisdn