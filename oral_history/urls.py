from django.conf.urls import url

from .views import OralHistoryIndexView, InterviewIndexView, InterviewView, UploadInterview, ThankYou, Error, UploadOHP, ThankYouOHP

urlpatterns = [
    url(r'^$', OralHistoryIndexView.as_view(), name='menu'),
    url(r'^(?P<slug>[-\w]+)/$', InterviewIndexView.as_view(), name='oral_history'),
    url(r'^(?P<slug>[-\w]+)/upload$', UploadInterview.as_view(), name='upload'),
    url(r'^(?P<slug>[-\w]+)/(?P<slug_interview>[-\w]+)$', InterviewView.as_view(), name='interview'),
    url(r'^upload', UploadOHP.as_view(), name='upload_ohp'),
    url(r'^thank-you', ThankYou.as_view(), name='thank_you'),
    url(r'^thank-you_ohp', ThankYouOHP.as_view(), name='thank_you_ohp'),
    url(r'^error', Error.as_view(), name='error'),
]
