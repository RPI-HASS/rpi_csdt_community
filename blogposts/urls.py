from django.conf.urls import url
from .views import (
    post_list,
    post_detail,
)

urlpatterns = [
    url(r'^$', post_list.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
]
