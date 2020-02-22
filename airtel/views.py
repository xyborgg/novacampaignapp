from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Download
from django.conf import settings
import json
import base64
# from device_detector import DeviceDetector
# from device_detector import SoftwareDetector

android_url = "https://play.google.com/store/apps/details?id=com.airtel.africa.selfcare"
ios_url = "https://apps.apple.com/us/app/my-airtel-africa/id1462268018?ls=1"

DEVICE = {
    'Android' : android_url,
    'Mac' : ios_url,
    'iOS': ios_url,
    'Windows': android_url
}

class Webairtel(View):

    def get(self, requests):
        """
        :param requests:
        :return:
        """
        influencer = requests.GET['influencer']
        decoded_info = "Airtel"
        final_url = "http://download.airtel.ng/checkinfluencer/?anchor=" + influencer
        return HttpResponseRedirect(final_url)


class Airtel(View):
    def get(self, requests):
        """
        :param requests:
        :return:
        """
        context = dict()
        ua = requests.META['HTTP_USER_AGENT']
        msisdn = requests.META.get('x-up-calling-line-id',None)
        device = ""
        if requests.Windows or requests.Linux:
            device = "Windows"
        if requests.Android:
            device = "Android"   
        if requests.iPhone  or requests.iPad:
            device = "iOS"
        if requests.iMac :
            device = "Mac"
        influencer = requests.GET['anchor']
        decoded_info = "Airtel"
        if influencer:
            decoded_info = base64.b64decode(influencer)
        context['influencer'] = influencer
        if msisdn is None:
            return render(requests,'airtel/enter_msisdn.html',context)
        device_type_url = DEVICE[device]
        res = Download.objects.create(msisdn=msisdn,device=device,influencer=str(decoded_info))
        if msisdn:
            res.msisdn = msisdn
            res.status = True
        else:
            res.msisdn = "NA"
            res.status = False
        res.save()
        data = {}
        return HttpResponseRedirect(DEVICE[device])


class EnterMsisdn(View):
    def get(self, request):
        context = dict()
        return render(request,'airtel/enter_msisdn.html',context)
    def post(self, request):
        msisdn = request.POST.get('msisdn',None)
        if msisdn is not None:
            device = ""
            if request.Windows or request.Linux:
                device = "Windows"
            if request.Android:
                device = "Android"   
            if request.iPhone  or request.iPad:
                device = "iOS"
            if request.iMac :
                device = "Mac"
            influencer = request.POST.get('influencer',None)
            decoded_info = "Airtel"
            if influencer:
                decoded_info = base64.b64decode(influencer)
            device_type_url = DEVICE[device]
            msisdn = '234%s' % msisdn[-10:]
            res = Download.objects.create(device=device,msisdn=msisdn,influencer=str(decoded_info))
            if msisdn:
                res.msisdn = msisdn
                res.status = True
            else:
                res.msisdn = "NA"
                res.status = False
            res.save()
            data = {}
            return HttpResponseRedirect(DEVICE[device])
        else:
            return redirect('enter_msisdn')