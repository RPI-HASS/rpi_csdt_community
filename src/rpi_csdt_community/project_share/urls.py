from django.conf.urls import patterns, url

from project_share.views import ProjectList, ApplicationList
from project_share.views import ProjectDetail
from project_share.views import ProjectCreate

urlpatterns = patterns('',
    url(r'^projects/$', ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'^projects/create$', ProjectCreate.as_view(), name='project-create'),
)
