# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Pictureurl, Analytics


class PictureUrlAdmin(admin.ModelAdmin):
    list_display = ["file_name", "date_created","title","image_path","auid", "details", "short_link", "hyperlink", "action"]


    class meta:
        model = Pictureurl


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('device', 'ip','campaign_url')
    list_filter = ('campaign_url',)

admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(Pictureurl, PictureUrlAdmin)
