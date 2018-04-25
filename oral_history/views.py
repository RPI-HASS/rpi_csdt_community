# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import DetailView

from .models import Interview, OralHistory

User = get_user_model()

# Create your views here.

class OralHistoryIndexView(ListView):
    template_name = 'menu.html'
    model = OralHistory

    def get_queryset(self):
        queryset = OralHistory.objects.all(approved=True)
        return queryset


class InterviewIndexView(ListView):
    template_name = 'oral_history.html'
    model = Interview

    def project(self):
        return OralHistory.objects.get(slug=self.kwargs['slug'])

    def get_queryset(self):
        queryset = Interview.objects.filter(project__slug=self.kwargs['slug'],approved=True)
        return queryset


class InterviewView(TemplateView):
    template_name = 'interview.html'

    def interview(self):
        return Interview.objects.get(slug=self.kwargs['slug_interview'])


class UploadInterview(LoginRequiredMixin, DetailView, FormView):
    template_name = 'upload.html'
    form_class = InterviewForm
    model = User
    
    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('thank_you'))

    def get_initial(self):
        return {
                }

    success_url = reverse_lazy('thank_you')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        form = InterviewForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            interview = form.save(commit=False)
            if request.FILES:
                interview.mp3_file = request.FILES['mp3_file']
                interview.pic = request.FILES['pic']
            interview.save()
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class InterviewView(TemplateView):
    template_name = 'thankyou.html'
