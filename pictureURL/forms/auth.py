from django import forms
from django.contrib.auth import ( authenticate, get_user_model )
from django.conf import settings
import requests
from django.forms import modelformset_factory

from pictureURL.models import Pictureurl


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=6, max_length=100, label=u'Password', required=True)





class UploadphotoForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ["title", "details", "hyperlink", "image_path", "action"

                  ]


class EditphotoForm(forms.ModelForm):
    class Meta:
        model = Pictureurl
        fields = ['title', "details", "image_path"

                  ]


EditphotoFormset = modelformset_factory(Pictureurl, form=EditphotoForm, extra=0)

class PublishForm(forms.Form):
    class Meta:
        model = Pictureurl
        fields = ['phonenumber', 'message']