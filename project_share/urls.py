from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from project_share.views import ProjectList, ProjectTagList, ApplicationList
from project_share.views import ProjectDetail, ApplicationDetail
from project_share.views import ProjectCreate, ApprovalCreate, AddressCreate
from project_share.views import AddressUpdate
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

    url(r'applications/$', ApplicationList.as_view(), name='application-list'),
    url(r'applications/(?P<pk>\d+)$', ApplicationDetail.as_view(), name='application-detail'),

    #url(r'users/(?P<pk>\d+)$', UserDetail.as_view(), name='user-detail'),
    url(r'users/(?P<pk>\d+)$', UserDetail.as_view(), name='extendeduser-detail'),
    
    url(r'address/create$', AddressCreate.as_view(), name='address-create'),
    url(r'address/confirm$', TemplateView.as_view(template_name='project_share/address_confirm.html'), name='address-confirm'),
    url(r'address/(?P<pk>.*)$', AddressUpdate.as_view(), name='address-update'),
)
