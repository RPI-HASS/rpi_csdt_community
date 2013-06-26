from django.conf.urls import patterns, url

from project_share.views import ProjectList, ApplicationList
from project_share.views import ProjectDetail, ApplicationDetail
from project_share.views import ProjectCreate
from project_share.views import ProjectJNLP

urlpatterns = patterns('',
    url(r'^projects/$', ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>\d+)/jnlp$', ProjectJNLP.as_view(), name='project-jnlp'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'^projects/create$', ProjectCreate.as_view(), name='project-create'),

    url(r'applications/(?P<pk>\d+)/jnlp$', ApplicationDetail.as_view(), name='application-detail'),
)
