from django import template
from django.db.models import Q

from project_share.models import Project

register = template.Library()


def unrestricted_projects(user, requester):
    try:
        obj = Project.objects.filter(Q(owner=user)).filter(Q(approved=True) | Q(owner=requester))
    except:
        obj = Project.objects.filter(Q(owner=user), Q(approved=True))
    return obj.all()


register = template.Library()
register.filter('unrestricted_projects', unrestricted_projects)
