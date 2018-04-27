from django.conf.urls import url

from .views import OralHistoryIndexView, InterviewIndexView, InterviewView, UploadInterview, ThankYou, Error

urlpatterns = [
    url(r'^$', OralHistoryIndexView.as_view(), name='oral_history_menu'),
    url(r'^(?P<slug>[-\w]+)/upload$', UploadInterview.as_view(), name='upload'),
    url(r'^(?P<slug>[-\w]+)/$', InterviewIndexView.as_view(), name='oral_history'),
    url(r'^(?P<slug>[-\w]+)/(?P<slug_interview>[-\w]+)$', InterviewView.as_view(), name='oral_history_interview'),
    url(r'^thank-you', ThankYou.as_view(), name='thank_you'),
    url(r'^error', Error.as_view(), name='error')
]