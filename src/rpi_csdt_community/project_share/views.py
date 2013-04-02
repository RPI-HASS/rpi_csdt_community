from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from project_share.models import Application, Project

class ApplicationList(ListView):
    model = Application

class ProjectList(ListView):
    model = Project

class ProjectDetail(DetailView):
    model = Project

class ProjectCreate(CreateView):
    model = Project
