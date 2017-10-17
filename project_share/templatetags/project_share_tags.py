from django import template
from django.db.models import Q

from project_share.models import Project


def unrestricted_projects(user, requester):
    try:
        obj = Project.objects.filter(Q(owner=user)).filter(Q(approved=True) | Q(owner=requester))
    except:
        obj = Project.objects.filter(Q(owner=user), Q(approved=True))
    return obj.all()


def get_ownership_object(ownership):
    ct = ownership.content_type
    return ct.get_object_for_this_type(pk=ownership.object_id)


register = template.Library()
register.filter('unrestricted_projects', unrestricted_projects)
register.filter('get_ownership_object', get_ownership_object)
