# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import View, UpdateView
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from scannerr.config import pagination
import uuid
from django.contrib.auth import logout as django_logout, authenticate, login, get_user_model
from pictureURL.forms.auth import UploadphotoForm, UserLoginForm,PublishForm,EditphotoForm
from .message import sendPostRequest
from .models import Pictureurl, Analytics
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib import messages
from . import bitly_api
import json
import requests

# Create your views here.


def login_page(request):
    ''' login view '''

    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    print("accepted details")
    if form.is_valid():
        print('form is valid')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            print('auth is valid')
            login(request, user)
        else:
            print('invalid auth')
            messages.add_message(request,messages.SUCCESS,"Incorrect username or password")
        print('auth')
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form
    }
    print("home details")
    return render(request,'login.html', context)

@login_required
def logout(request):
    django_logout(request)
    return redirect('/login')

''' 
    Dashboard View 
'''
@login_required
def dashboard(request, template='new/home.html'):
    # allphoto = Pictureurl.objects.all()

    context = {'title':'Dashboard',
               'user':request.user,
               # "allphoto": allphoto,
               }
    return render(request, template, context)

class Upload_Campaign(View):
    form_class = UploadphotoForm
    template = 'new/campaign.html'

    def get(self, request):
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'Upload Campaign'
                   }
        return render(request, self.template, context)

    def post(self, request):
        #form = self.form_class(request.POST)
        # if form.is_valid():
        image_ext = [".jpeg", ".jpg", ".gif", ".png"]
        video_ext = [".avi", ".mp4", ".flv", ".mpeg", ".swf", ".mpg", ".mpe", ".mov", ".wmv", ".ogg", "3gp"]

        print ("form is valid")
        picture = Pictureurl()
        picture.title = request.POST.get('title')
        picture.details = request.POST.get('details')
        picture.date_created = datetime.now()
        picture.auid = str(uuid.uuid4())
        new_file_name = picture.auid

        file_url = 'https://' + os.environ.get('APP_HOST') + f'/campaign/{new_file_name}'
        try:
            bitly_client = bitly_api.Connection(access_token='41e1370eaa1d74350310ef25a91fa05793015dc5')
            response = bitly_client.shorten(uri=file_url)
            short_link = response.get('url')
            picture.short_link = short_link if short_link else file_url
        except Exception:
            picture.short_link = file_url

        _file = request.FILES['file']
        picture.file_name = _file.name
        file_extension = os.path.splitext(_file.name)[1]
        media_type = None
        if file_extension in image_ext:
            media_type = 'image'
        elif file_extension in video_ext:
            media_type = 'video'

        if not media_type:
            messages.add_message(request, messages.ERROR, "Invalid Media Uploaded - Only Image | Video Supported")
            return redirect('/NewCampaign')
        new_file_path = os.path.join(settings.MEDIA_URL, "%s" % new_file_name) + file_extension
        print ("starting to upload file ")
        with open(new_file_path, 'wb+') as destination:
            for chunk in _file.chunks():
                destination.write(chunk)
        picture.image_path = new_file_name + file_extension



        print("saving to db")
        picture.save()
        print('file uploaded')
        return redirect("campaign_list")


''' all  campaigns view  '''
def campaign_list(request):
    template = 'New/Manage-Campaigns.html'
    allphoto = Pictureurl.objects.all()
    paginator = Paginator(allphoto, 5)
    host = request.get_host
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        "allphoto": items,
        'title': 'All Campaigns',

    }

    print(host)
    return render(request, template, context)

def campaigndetail(request, auid,):
    template = 'campaign-detail.html'
    details = Pictureurl.objects.get(auid=auid)
    context = {

        'details': details,
        'title': ' Details',
    }
    return render(request, template, context)



def search(request):
    template = "AllCampaigns.html"
    query = request.GET.get('q')
    result = Pictureurl.objects.filter(Q(title__icontains=query))
    context = {
        "allphoto": result
    }
    print(context)
    return render(request, template, context)


class EditCampaign(UpdateView):
    template = "campaign-edit.html"
    form_class = EditphotoForm
    queryset = Pictureurl.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Pictureurl, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def edit(request, id):
    template = "campaign-edit.html"
    post = get_object_or_404(Pictureurl, id=id)
    if request.method == "POST":
        form = UploadphotoForm(request.POST, instance=g )
        try:
            if form.is_valid():
                form.save()
                messages.SUCCESS(request, "Your Campaign Was Edited")
                # return redirect('campaigndetail')
        except Exception as e:
            messages.warning(request, "Your Campaign Was Not Edited")
    else:
        form = EditphotoForm(instance=post)

    context = {
          'form': form,
            'post': post,
        }

    return render(request, template, context)




def delete_campaign(request,pk):
    if request.method == 'GET':
        photo = Pictureurl.objects.get(pk=pk)
        print("the delete")
        photo.delete()
    return redirect('campaign_list')


def campaign(request, auid):
    if Pictureurl.objects.filter(auid=auid).exists():
        model = Pictureurl.objects.get(auid=auid)
        context = dict()
        context['model'] = model
        return render(request, "campaign.html",context)
    else:
        return Http404

def calender(request):
    context = {
        'title': 'Calender'
    }
    return render(request, 'calendar.html', context)


class Publish(View):
    form_class = PublishForm
    template = "smsform.html"


    def get(self, request, auid ):
        details = Pictureurl.objects.get(auid=auid)
        form = self.form_class(None)
        context = {'form': form,
                   'title': 'Publish',
                   'details': details,
                   }
        return render(request, self.template, context)

    def post(self, request):
        url = "https://www.bulksmsnigeria.com/api/v1/sms/create"
        phone = request.POST.get('phonenumber')
        message = request.POST.get('message')
        to = f"{phone}"
        body = f"{message}"
        print(to)
        print(body)

        response = sendPostRequest(url, "P0KpZxWPZwOIT6JIKEBCFOFE6Q12ztUrsbCoxdE2ppfsXRwqAUyx3kEvTYFy", "Nova360", to, body)
        print(response.text)
        return redirect("campaign_list")


# def textform(request):
#     template = "smsform.html"
#     return render(request, template)
#
#
# url = "https://www.bulksmsnigeria.com/api/v1/sms/create"
#
# def sendPostRequest(requrl, api_token ,FROM, to, body):
#
#     req_params = {
#         "api_token": api_token,
#         "from": FROM,
#         "to": "234" + to,
#         "body": body
#     }
#
#     return requests.post(requrl, req_params)
#
#
# def postmessage(request):
#     phone = request.GET.get('phone')
#     message = request.GET.get('text')
#     to = f"{phone}"
#     body = f"{message}"
#
#     response = sendPostRequest(url, "P0KpZxWPZwOIT6JIKEBCFOFE6Q12ztUrsbCoxdE2ppfsXRwqAUyx3kEvTYFy", "Nova360",
#                                to, body)
#     return render(request, )