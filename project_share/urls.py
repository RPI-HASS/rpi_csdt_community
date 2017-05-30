"""Directs URLs for the project_share sub-app to relevant views."""
from django.conf.urls import url
from django.views.generic.base import TemplateView

from project_share.views import (AddressCreate, AddressUpdate,
                                 ApplicationDetail, ApplicationList,
                                 ApplicationRunDetail, ApprovalCreate,
                                 DemoDetail, DemoList, ProjectCreate,
                                 ProjectDelete, ProjectDetail, ProjectList,
                                 ProjectPresentDetail, ProjectRunDetail,
                                 ProjectTagList, ProjectUnpublish,
                                 ProjectUpdate, UserDetail)

urlpatterns = [
    url(r'^projects/$', ProjectList.as_view(), name='project-list'),
    url(r'^projects/tag/(?P<tag_pk>\d+)/$', ProjectTagList.as_view(), name='project-tag-list'),
    url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
    url(r'^projects/(?P<pk>\d+)/run$', ProjectRunDetail.as_view(), name='project-run-detail'),
    url(r'^projects/(?P<pk>\d+)/present$', ProjectPresentDetail.as_view(), name='project-present-detail'),
    url(r'^projects/create$', ProjectCreate.as_view(), name='project-create'),
    url(r'^projects/(?P<pk>\d+)/edit$', ProjectUpdate.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>\d+)/delete$', ProjectDelete.as_view(), name='project-delete'),
    url(r'^projects/(?P<pk>\d+)/unpublish$', ProjectUnpublish.as_view(), name='project-unpublish'),
    url(r'^projects/delete/success$',
        TemplateView.as_view(template_name='project_share/project_delete_success.html'),
        name='project-delete-success'),
    url(r'^projects/unpublish/success$',
        TemplateView.as_view(template_name='project_share/project_unpublish_success.html'),
        name='project-unpublish-success'),

    url(r'projects/(?P<project_pk>\d+)/publish$', ApprovalCreate.as_view(), name='approval-create'),
    url(r'approval/confirm$', TemplateView.as_view(template_name='project_share/approval_confirm.html'),
        name='approval-confirm'),

    url(r'applications/$', ApplicationList.as_view(), name='application-list'),
    url(r'applications/(?P<pk>\d+)$', ApplicationDetail.as_view(), name='application-detail'),
    url(r'applications/(?P<pk>\d+)/run$', ApplicationRunDetail.as_view(), name='application-run-detail'),

    url(r'^demos/$', DemoList.as_view(), name='demo-list'),
    url(r'^demos/(?P<pk>\d+)$', DemoDetail.as_view(), name='demo-detail'),

    url(r'users/(?P<pk>\d+)$', UserDetail.as_view(), name='extendeduser-detail'),

    url(r'address/create$', AddressCreate.as_view(), name='address-create'),
    url(r'address/confirm$', TemplateView.as_view(template_name='project_share/address_confirm.html'),
        name='address-confirm'),
    url(r'address/(?P<pk>.*)$', AddressUpdate.as_view(), name='address-update'),
]
