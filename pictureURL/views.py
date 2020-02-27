# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, ListView
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from scannerr.config import pagination
import uuid
from django.contrib.auth import logout as django_logout, authenticate, login, get_user_model
from pictureURL.forms.auth import UploadphotoForm, UserLoginForm,PublishForm,EditphotoForm, EditphotoFormset
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
def dashboard(request):
    template = 'home.html'

    context = {'title':'Dashboard',
               'user': request.user,
               }
    return render(request, template, context)





class Upload_Campaign(View):
    form_class = UploadphotoForm
    template = 'campaign.html'
    success_url = reverse_lazy('campaign_list')

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
        picture.hyperlink = request.POST.get('hyperlink')
        picture.action =  request.POST.get('action')
        picture.date_created = datetime.now()
        picture.auid = str(uuid.uuid4())
        new_file_name = picture.auid

        file_url = 'https://{hostname}/campaign/{filename}'.format(
            hostname=os.environ.get('APP_HOST'),
            filename =new_file_name)
        print(file_url)
        try:
            bitly_client = bitly_api.Connection(access_token='41e1370eaa1d74350310ef25a91fa05793015dc5')
            response = bitly_client.shorten(uri=file_url)
            short_link = response.get('url')
            print(short_link)
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
    template = 'Manage-Campaigns.html'
    user_list = Pictureurl.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'title': 'All Campaigns',
        "items": items
    }


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

#
# class EditCampaign(UpdateView):
#     template = "campaign-edit.html"
#     form_class = EditphotoForm
#     queryset = Pictureurl.objects.all()
#
#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         campaign =get_object_or_404(Pictureurl, id=id_)
#         queryset = Pictureurl.objects.filter(item=item)
#
#
#     def form_valid(self, form):
# #         print(form.cleaned_data)
#         return super().form_valid(form)

class EditListView(ListView):
    model = Pictureurl
    items = Pictureurl.objects.all()
    template_name = 'campaign-edit.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EditListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edit'
        context['formset'] = EditphotoFormset(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        # breakpoint()
        item_pk = self.kwargs["id"]
        item = get_object_or_404(Pictureurl, pk=item_pk)
        print(item)
        queryset = Pictureurl.objects.filter(
            item=item)
        return queryset
        # return item

    def post(self, request, *args, **kwargs):
        formset = EditphotoFormset(request.POST, request.FILES)
        print(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                item_pk = self.kwargs.get("id")
                item = get_object_or_404(Pictureurl, pk=item_pk)
                new_item.item = item
                new_item.save()
            messages.success(request, "Your Campaign and pricing has been updated.")
            return redirect("campaign_list")
        raise Http404


#
# def edit(request, id):
#     template = "campaign-edit.html"
#     post = get_object_or_404(Pictureurl, id=id)
#     if request.method == "POST":
#         form = UploadphotoForm(request.POST, instance=g )
#         try:
#             if form.is_valid():
#                 form.save()
#                 messages.SUCCESS(request, "Your Campaign Was Edited")
#                 # return redirect('campaigndetail')
#         except Exception as e:
#             messages.warning(request, "Your Campaign Was Not Edited")
#     else:
#         form = EditphotoForm(instance=post)
#
#     context = {
#           'form': form,
#             'post': post,
#         }
#
#     return render(request, template, context)




def delete_campaign(request,pk):
    if request.method == 'GET':
        photo = Pictureurl.objects.get(pk=pk)
        print("the delete")
        photo.delete()
    return redirect('campaign_list')


def campaign(request, auid):
    template = 'ads.html'
    if Pictureurl.objects.filter(auid=auid).exists():
        model = Pictureurl.objects.get(auid=auid)
        context = dict()
        context['model'] = model
        return render(request, template ,context)
    else:
        return Http404


class Publish(View):
    form_class = PublishForm
    template = "smsform.html"


    def get(self, request):
        details = Pictureurl.objects.all()
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


class Analytic (View):
    model = Analytics

    def get(self, requests):
        """
        :param requests:
        :return:
        """
        obj = get_object_or_404()

        Analytics.ip = requests.META.get('HTTP_X_FORWARDED_FOR')
        x_forwarded_for = Analytics.ip
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = requests.META.get('REMOTE_ADDR')

        ua = requests.META['HTTP_USER_AGENT']
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

        return HttpResponseRedirect(device)