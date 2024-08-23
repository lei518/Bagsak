from django import forms
from django.forms import ModelForm
from .models import Announcement

class Announcementform(ModelForm):
    class Meta:
        model = Announcement
        fields = ('content',)
