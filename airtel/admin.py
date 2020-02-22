from django.contrib import admin

# Register your models here.
from .models import Download
# Register your models here.


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('msisdn', 'status','device', 'influencer', 'date_created')
    list_filter = ('status',)

admin.site.register(Download, DownloadAdmin)