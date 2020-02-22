from django import forms
from django.contrib.auth import ( authenticate, get_user_model )
from django.conf import settings
import requests
from pictureURL.models import Pictureurl


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=6, max_length=100, label=u'Password', required=True)





class UploadphotoForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ['title', "details", "image_path"

                  ]


class EditphotoForm(forms.ModelForm):
    class Meta:
        model = Pictureurl
        fields = ['title', "details", "image_path"

                  ]


class PublishForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ['phonenumber', 'message']