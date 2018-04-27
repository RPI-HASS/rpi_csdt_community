# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import DetailView

from .models import Interview, OralHistory
from .forms import InterviewForm

User = get_user_model()

# Create your views here.

class OralHistoryIndexView(ListView):
    template_name = 'oral_history/menu.html'
    model = OralHistory

    def get_queryset(self):
        queryset = OralHistory.objects.all()
        return queryset


class InterviewIndexView(ListView):
    template_name = 'oral_history/oral_history.html'
    model = Interview

    def slug_return(self):
        return self.kwargs['slug']

    def project(self):
        return OralHistory.objects.filter(slug=self.kwargs['slug'])

    def get_queryset(self):
        queryset = Interview.objects.filter(project__slug=self.kwargs['slug'],approved=True)
        return queryset


class InterviewView(TemplateView):
    template_name = 'oral_history/interview.html'

    def slug_return(self):
        return self.kwargs['slug']

    def slug_interview_return(self):
        return self.kwargs['slug_interview']

    def interview(self):
        return Interview.objects.filter(slug=self.kwargs['slug_interview'])


class UploadInterview(LoginRequiredMixin, DetailView, FormView):
    template_name = 'oral_history/upload.html'
    form_class = InterviewForm
    model = User
    
    def get_object(self, queryset=None):
        pass

    # def get_object(self, queryset=None):
    #     return self.request.user

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('oral_history:thank_you'))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('oral_history:error'))

    def get_initial(self):
        initial = super(UploadInterview, self).get_initial()
        try:
            original_project = OralHistory.objects.get(slug=self.kwargs['slug'])
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['project'] = original_project
        return initial


    success_url = reverse_lazy('oral_history:thank_you')

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object() 
        form = InterviewForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)

            if request.FILES:
                form.mp3_file = request.FILES['mp3_file']
                form.pic = request.FILES['pic']
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ThankYou(TemplateView):
    template_name = 'oral_history/thankyou.html'


class Error(TemplateView):
    template_name = 'oral_history/error.html'
