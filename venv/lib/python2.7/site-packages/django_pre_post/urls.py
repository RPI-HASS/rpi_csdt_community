from django.conf.urls import include, url
from django.contrib import admin
from django_pre_post.views import FillOutQuestionnaire, FramelessQuestionnaire
from django_pre_post.viewsets import AttemptViewSet
from django.views.generic.base import TemplateView

from rest_framework import routers
router = routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'attempts', AttemptViewSet, base_name='api-attempts')

urlpatterns = [
    url(r'^questionnaire/(?P<pk>\d+)/$', FillOutQuestionnaire.as_view(), name='fill-out-questionnaire'),
    url(r'^success/',
        TemplateView.as_view(template_name='django_pre_post/successful_post.html'),
        name='successful-submission'),
    url(r'^embed-questionnaire/(?P<pk>\d+)/$', FramelessQuestionnaire.as_view(), name='embed-questionnaire'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
