from django.conf.urls import url
from . import views

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    url(r'^tag/(?P<tag>[\w-]+)/$', views.ViewTag.as_view(), name='tag'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.DateSearch.as_view(), name='date'),
    # url(r'^posts/$', "<appname>.views.<function_name>"),
]
