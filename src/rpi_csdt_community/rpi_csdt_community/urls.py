from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registration.backends.simple.views import RegistrationView

from rpi_csdt_community.forms import CaptchaRegistrationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # TemplateView + Login
    #url(r'^$', login_required(TemplateView.as_view(template_name="home.html")), {}, 'home'),
    url(r'^$', 'rpi_csdt_community.views.home', {}, 'home'),

    url(r'', include('project_share.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'home.html'}),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=CaptchaRegistrationForm), name='registration_register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/', RedirectView.as_view(url='/')),
    url(r'^accounts/profile/', RedirectView.as_view(url='/')),

    url(r'^comments/', include('django_comments_xtd.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
