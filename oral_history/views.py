# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import DetailView


from .models import Interview, OralHistory
from .forms import InterviewForm, OHPForm
from project_share.models import Project, FileUpload, Application

from django_teams.models import Team


User = get_user_model()

# Create your views here.


class OralHistoryIndexView(ListView):
    template_name = 'oral_history/menu.html'
    model = OralHistory

    def get_queryset(self):
        queryset = OralHistory.objects.filter(is_official=True, approved=True)
        return queryset
    
    def get_classrooms(self):
        return OralHistory.objects.filter(is_official=False, approved=True)


class InterviewIndexView(ListView):
    template_name = 'oral_history/oral_history.html'
    model = Interview

    def slug_return(self):
        return self.kwargs['slug']

    def project(self):
        return OralHistory.objects.filter(slug=self.kwargs['slug'])

    def get_queryset(self):
        queryset = Interview.objects.filter(project__slug=self.kwargs['slug'], approved=True)
        return queryset


class InterviewView(TemplateView):
    template_name = 'oral_history/interview.html'

    def slug_return(self):
        return self.kwargs['slug']

    def slug_interview_return(self):
        return self.kwargs['slug_interview']

    def get_context_data(self, **kwargs):
        context = super(InterviewView, self).get_context_data(**kwargs)
        context['interview_context'] = Interview.objects.filter(slug=self.kwargs['slug_interview'])
        return context


class UploadInterview(LoginRequiredMixin, DetailView, FormView):
    template_name = 'oral_history/upload.html'
    form_class = InterviewForm
    success_url = reverse_lazy('oral_history:thank_you')

    def get_object(self, queryset=None):
        pass

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
        initial['user'] = self.request.user
        # classrooms = Team.objects.filter(users=self.request.user)
        # initial['classrooms'] = classrooms
        return initial

    def get_slug(self):
        return self.kwargs['slug']

    def get_form_kwargs(self):
        kwargs = super(UploadInterview, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = InterviewForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            new_interview = form.save(commit=False)
            if request.FILES:
                form.mp3_file = request.FILES['mp3_file']
                form.pic = request.FILES['pic']
            
            text_dump = json.dumps([self.kwargs['slug'], slugify(form.cleaned_data['full_name'])])
            project_blob = FileUpload(file_path=text_dump)
            project_blob.save()
            image_blob = FileUpload(file_path=form.pic)
            image_blob.save()
            # find curr classroom
            # classroom =
            application = Application.objects.get(id=70)
            classroom = Team.objects.get(pk=form.cleaned_data['classroom'])
            new_proj = Project(name=form.cleaned_data['full_name'], description=form.cleaned_data['summary'], owner=request.user,
                                  application=application, project=project_blob, classroom=classroom, screenshot=image_blob, )
            new_proj.save()
            # save_proj = Project.objects.get(id=new_proj.id)
            # print('save_proj', save_proj)
            # TODO: Not working
            new_interview.csdt_project = new_proj
            new_interview.save()
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UploadOHP(LoginRequiredMixin, DetailView, FormView):
    template_name = 'oral_history/upload_ohp.html'
    form_class = OHPForm
    success_url = reverse_lazy('oral_history:thank_you')

    def get_object(self, queryset=None):
        pass

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('oral_history:thank_you_ohp'))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('oral_history:error'))

    def get_initial(self):
        initial = super(UploadOHP, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self):
        kwargs = super(UploadOHP, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = OHPForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            new_ohp = form.save(commit=False)
            if request.FILES:
                form.pic = request.FILES['pic']
            new_ohp.save()
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ThankYou(TemplateView):
    template_name = 'oral_history/thankyou.html'


class ThankYouOHP(TemplateView):
    template_name = 'oral_history/thankyou.html'


class Error(TemplateView):
    template_name = 'oral_history/error.html'
