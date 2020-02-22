from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from pictureURL.views import *
from . import views

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", login_page , name="login_page"),
    path('logout/', logout, name='logout'),
    path("AllCampaigns/", campaign_list, name="campaign_list"),
    path('campaigndetail/<slug:auid>', campaigndetail, name='campaigndetail'),
    path("NewCampaign/", views.Upload_Campaign.as_view(),  name="upload_photo"),
    path("Edit/<int:id>/update", edit, name="edit_campaign"),
    path("Delete_Campaign/<int:pk>/", delete_campaign, name="delete_campaign"),
    path("smsform/<slug:auid>", Publish.as_view(),  name="textform"),
    path("Result/", search, name="search"),
    path("Calender/", calender, name="calender")


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
