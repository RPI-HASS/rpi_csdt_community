from django.conf.urls import url
from .views import (
    EntryListView
)

urlpatterns = [
    url(r'^$', EntryListView.as_view(), name='list'),
]
