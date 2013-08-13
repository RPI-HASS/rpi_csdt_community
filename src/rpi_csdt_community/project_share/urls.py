from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from project_share.views import ProjectList, ProjectTagList
from project_share.views import ProjectDetail, ApplicationDetail
from project_share.views import ProjectCreate, ApprovalCreate
from project_share.views import ProjectUpdate
from project_share.views import ProjectDelete
from project_share.views import ProjectJNLP
from project_share.views import UserDetail

urlpatterns = patterns('',
    url(r'^projects/$', ProjectList.as_view(), name='project-list'),
    url(r'^projects/tag/(?P<tag_pk>\d+)/$', ProjectTagList.as_view(), name='project-tag-list'),
    url(r'^projects/(?P<pk>\d+)/jnlp$', ProjectJNLP.as_view(), name='project-jnlp'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'^projects/create$', ProjectCreate.as_view(), name='project-create'),
    url(r'^projects/(?P<pk>\d+)/edit$', ProjectUpdate.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>\d+)/delete$', ProjectDelete.as_view(), name='project-delete'),
    url(r'^projects/delete/success$', TemplateView.as_view(template_name='project_share/project_delete_success.html'), name='project-delete-success'),

    url(r'projects/(?P<project_pk>\d+)/publish$', ApprovalCreate.as_view(), name='approval-create'),
    url(r'approval/confirm$', TemplateView.as_view(template_name='project_share/approval_confirm.html'), name='approval-confirm'),

    url(r'applications/(?P<pk>\d+)/jnlp$', ApplicationDetail.as_view(), name='application-detail'),

    url(r'users/(?P<pk>\d+)$', UserDetail.as_view(), name='user-detail'),
)
