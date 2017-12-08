from django import template
from django.db.models import Q
from project_share.models import Project
from django.contrib.staticfiles import finders
register = template.Library()


def unrestricted_projects(user, requester):
    try:
        obj = Project.objects.filter(Q(owner=user)).filter(Q(approved=True) | Q(owner=requester))
    except:
        obj = Project.objects.filter(Q(owner=user), Q(approved=True))
    return obj.all()


def get_ownership_object(ownership):
    ct = ownership.content_type
    return ct.get_object_for_this_type(pk=ownership.object_id)


@register.simple_tag
def includestatic(path, encoding='UTF-8'):
    file_path = finders.find(path)
    with open(file_path, "r") as f:
        string = f.read()
        return string


register.filter('unrestricted_projects', unrestricted_projects)
register.filter('get_ownership_object', get_ownership_object)
