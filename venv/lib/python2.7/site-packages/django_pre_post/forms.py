from django import forms
from django_pre_post.models import Questionnaire


class CSRFQuestionnaireForm(forms.Form):
    model = Questionnaire
    fields = []
