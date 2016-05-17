from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from project_share.models import Project

from django.conf import settings
register = template.Library()

def unrestricted_projects(user, requester):
    try:
        o = Project.objects.filter(Q(owner=user)).filter(Q(approved=True) | Q(owner=requester))
    except:
        o = Project.objects.filter(Q(owner=user), Q(approved=True))
    return o.all()

register = template.Library()
register.filter('unrestricted_projects', unrestricted_projects)