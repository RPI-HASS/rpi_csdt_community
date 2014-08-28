from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rpi_csdt_community.forms import CaptchaRegistrationForm

from rpi_csdt_community.views import RedirectRegistrationView

from django.contrib import admin
admin.autodiscover()

from rpi_csdt_community.viewsets import ProjectViewSet, DemosViewSet, GoalViewSet, FileUploadView, CurrentUserView
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='api-projects')
router.register(r'demos', DemosViewSet, base_name='api-demos')
router.register(r'goals', GoalViewSet, base_name='api-goals')

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # TemplateView + Login
    #url(r'^$', login_required(TemplateView.as_view(template_name="home.html")), {}, 'home'),
    url(r'^$', 'rpi_csdt_community.views.home', {}, 'home'),

    url(r'', include('project_share.urls')),
    url(r'teams/', include('django_teams.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'home.html'}),
    url(r'^accounts/register/$', RedirectRegistrationView.as_view(form_class=CaptchaRegistrationForm), name='registration_register'),
    url(r'^accounts/chpasswd/done/?', 'django.contrib.auth.views.password_change_done', {'template_name':'password_change_done.html'}),
    url(r'^accounts/change/password/?', 'django.contrib.auth.views.password_change', {'template_name':'change_password.html', 'post_change_redirect': '/accounts/chpasswd/done/' }, name="change_password"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/', RedirectView.as_view(url='/')),
    url(r'^accounts/profile/', RedirectView.as_view(url='/')),

    url(r'^comments/', include('django_comments_xtd.urls')),

    (r'^attachments/', include('attachments.urls')),
    (r'^likes/', include('likes.urls')),
    (r'^forum/', include('pybb.urls', namespace='pybb')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api/files/', FileUploadView.as_view(), name='file-create'),
    url(r'^api/user', CurrentUserView.as_view(), name='user-api-detail')
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
