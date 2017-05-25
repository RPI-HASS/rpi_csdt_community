from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.conf import settings
import debug_toolbar

from django.contrib import admin
admin.autodiscover()

from rpi_csdt_community.viewsets import ProjectViewSet, DemosViewSet, GoalViewSet, ApplicationViewSet, FileUploadView, CurrentUserView, TeamViewSet
from rpi_csdt_community.viewsets import ApplicationThemeViewSet, ApplicationCategoryViewSet
from rpi_csdt_community.views import home
from django.views import static
from django.views.static import serve

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='api-projects')
router.register(r'team', TeamViewSet, base_name='api-teams')
router.register(r'demos', DemosViewSet, base_name='api-demos')
router.register(r'goals', GoalViewSet, base_name='api-goals')
router.register(r'application', ApplicationViewSet, base_name='api-modules')
router.register(r'theme', ApplicationThemeViewSet, base_name='api-themes')
router.register(r'category', ApplicationCategoryViewSet, base_name='api-category')

		
urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # TemplateView + Login
    url(r'^(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT+'/index.html'}),
    #url(r'^$', home, {}, 'home'),
    #url(r'^$', login_required(TemplateView.as_view(template_name="home.html")), {}, 'home'),

    url(r'', include('project_share.urls')),
    url(r'teams/', include('django_teams.urls')),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^comments/', include('django_comments_xtd.urls')),

    url(r'^attachments/', include('attachments.urls', namespace="attachments")),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api/files/', FileUploadView.as_view(), name='file-create'),
    url(r'^api/user', CurrentUserView.as_view(), name='user-api-detail'),

    url(r'^cms/', include('cms.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT,}),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT,}),
]

if settings.ENABLE_GIS:
    urlpatterns += [
        url(r'^api-gis/', include('gis_csdt.urls')),
        url(r'^gis/', TemplateView.as_view(template_name='gis.html')),
    ]
