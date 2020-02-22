from airtel.views import EnterMsisdn, Airtel, Webairtel
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [

    url(r'^advertapp/', Webairtel.as_view()),
    url(r'^checkinfluencer/', Airtel.as_view()),
    url(r'^enter-msisdn/', EnterMsisdn.as_view(), name='enter_msisdn'),

]