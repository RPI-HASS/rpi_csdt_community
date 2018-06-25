from django.conf.urls import url

from .views import (OralHistoryIndexView,
                    InterviewIndexView, InterviewView, UploadInterview,
                    ThankYou, Error, UploadOHP, ThankYouOHP,
                    ThankYouTag, InterviewUpdate, OHPUpdate)

urlpatterns = [
    url(r'^$', OralHistoryIndexView.as_view(), name='menu'),
    url(r'^(?P<slug>[-\w]+)/$', InterviewIndexView.as_view(), name='oral_history'),
    url(r'^(?P<slug>[-\w]+)/upload$', UploadInterview.as_view(), name='upload'),
    url(r'^(?P<slug>[-\w]+)/update$', OHPUpdate.as_view(), name='update_ohp'),
    url(r'^(?P<slug>[-\w]+)/(?P<slug_interview>[-\w]+)$', InterviewView.as_view(), name='interview'),
    url(r'^(?P<slug>[-\w]+)/(?P<slug_interview>[-\w]+)/update$', InterviewUpdate.as_view(), name='interview_update'),
    url(r'^upload', UploadOHP.as_view(), name='upload_ohp'),
    url(r'^thank-you', ThankYou.as_view(), name='thank_you'),
    url(r'^thank-you_ohp', ThankYouOHP.as_view(), name='thank_you_ohp'),
    url(r'^(?P<slug>[-\w]+)/(?P<slug_interview>[-\w]+)/thank-you_tag', ThankYouTag.as_view(), name='thank_you_tag'),
    url(r'^error', Error.as_view(), name='error'),
]
