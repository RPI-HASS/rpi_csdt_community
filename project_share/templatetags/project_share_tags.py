'''Template Tags for Project_Share'''
from django import template
from django.db.models import Q

from project_share.models import Project


register = template.Library()


def unrestricted_projects(user, requester):
    '''Queryset for Unrestricted Projects'''
    try:
        objects_retrieved = \
            Project.objects.filter(Q(owner=user)).filter(Q(approved=True)
                                                         | Q(owner=requester))
    except:
        objects_retrieved = Project.objects.filter(Q(owner=user), Q(approved=True))
    return objects_retrieved.all()


register = template.Library()
register.filter('unrestricted_projects', unrestricted_projects)
