'''RPI CSDT Community Views.py'''

from django_comments.views.comments import post_comment
from django.contrib.auth.forms import AuthenticationForm
# from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
# from django.template import RequestContext

from project_share.models import Project


def comment_post_wrapper(request):
    '''Comment Post Wrapper'''
    # Clean the request to prevent form spoofing
    if request.user.is_authenticated():
        if not (request.user.get_full_name() == request.POST['name'] or \
               request.user.email == request.POST['email']):
            return HttpResponse("Error 403: You're an evil hacker")
        return post_comment(request)
    return HttpResponse("Error 403: You're an evil hacker")


def home(request):
    '''Helps render the homescreen with Popular and Newest projects'''
    # Get the 10 most popular projects
    # Get the 10 newest
    projects_newest = \
        Project.approved_projects().all().select_related("screenshot").order_by('-id')[:10]
    projects_newest = [project for project in projects_newest]
    return render(request, 'home.html', {
        "form": AuthenticationForm(),
        'projects_popular': projects_newest,
        'projects_newest': projects_newest
    })


def return_true():
    '''Return True'''
    return True
