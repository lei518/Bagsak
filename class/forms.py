from django import forms
from django.forms import ModelForm
from .models import Announcement, Materials

class Announcementform(ModelForm):
    class Meta:
        model = Announcement
        fields = ('content',)

class Materialsform(ModelForm):
    class Meta:
        model = Materials
        fields = ('course', 'title', 'description', 'content', 'created_by', )