"""Display the id, name, description, and url for the demo."""
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django_comments.views.comments import post_comment
from project_share.models import Application, Project


def comment_post_wrapper(request):
    """Clean the request to prevent form spoofing."""
    if request.user.is_authenticated:
        if not (request.user.get_full_name() == request.POST['name'] or
                request.user.email == request.POST['email']):
            return HttpResponse("Error 403: You're an evil hacker")
        return post_comment(request)
    return HttpResponse("Error 403: You're an evil hacker")


def home(request):
    """Get the 10 most popular projects *dead*, Get the 10 newest."""
    projects_newest = Project.approved_projects().all().select_related("screenshot").order_by('-id')[:10]
    projects_newest = [project for project in projects_newest]
    return render(request, 'home.html', {
        "form": AuthenticationForm(),
        'projects_popular': projects_newest,
        'projects_newest': projects_newest
    })


# Replaced cards with Angular ApplicationList
class Home(ListView):
    model = Application
    template_name = "home.html"

    def get_queryset(self):
        cache_key = 'ApplicationListForHome'
        cache_time = 1800  # time to live in seconds
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Application.objects.filter(featured=True).order_by('rankApp', 'name')
            cache.set(cache_key, queryset, cache_time)
        return queryset


class ReactAppList(ListView):
    model = Application
    template_name = "project_share/application_list_react.html"


class About(TemplateView):
    template_name = "rpi_csdt_community/about.html"


class Guides(TemplateView):
    template_name = "rpi_csdt_community/guides.html"
