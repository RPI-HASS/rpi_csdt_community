from django import forms
from django.forms import ModelForm

from project_share.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('owner',)
