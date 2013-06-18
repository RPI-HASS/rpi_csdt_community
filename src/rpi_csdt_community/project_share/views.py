from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from project_share.models import Application, Project
from project_share.forms import ProjectForm

class ApplicationList(ListView):
    model = Application

class ApplicationDetail(DetailView):
    model = Application

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update({'content_type': 'application/x-java-jnlp-file'})
        return super(ApplicationDetail, self).render_to_response(context, **response_kwargs)

class ProjectList(ListView):
    model = Project

class ProjectDetail(DetailView):
    model = Project

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
      self.kwargs = kwargs
      self.request = request
      return super(ProjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
      form.instance.owner = self.request.user
      return super(ProjectCreate, self).form_valid(form)

