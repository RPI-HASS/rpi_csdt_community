from django.conf.urls import include, url
from rest_framework import routers
from gis_csdt import views, templates
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'api-ds', views.DatasetViewSet)
router.register(r'api-location', views.LocationViewSet, base_name='location')
router.register(r'api-geocoor', views.GeoCoordinatesViewSet,
                base_name='geocoor')
router.register(r'rpi-dsnames', views.DatasetNameFieldViewSet,
                base_name='ds_names')
router.register(r'api-mp', views.MapPointViewSet, base_name='mappoint')
router.register(r'api-newtag', views.NewTagViewSet)
router.register(r'api-poly', views.MapPolygonViewSet, base_name='mappolygon')
router.register(r'api-tag', views.NewTagViewSet)
router.register(r'api-test', views.TestView, base_name='mp')
router.register(r'api-count', views.CountPointsInPolygonView,
                base_name='count_points')
# router.register(r'api-tag/count', views.TagCountViewSet, base_name = 'tag')
router.register(r'api-dist', views.AnalyzeAreaAroundPointView,
                base_name='area')
router.register(r'api-dist2', views.AnalyzeAreaAroundPointNoValuesView,
                base_name='area2')
router.register(r'api-newsensor', views.NewSensorView)
router.register(r'api-datapoint', views.SubmitDataPointView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api-SMS', views.SMSSubmitDataPointView, name='SMS-data'),
    url(r'api-addmp', views.AddMapPointView.as_view(), name='Add_MP'),
    url(r'api-addds', views.AddDatasetView.as_view(), name='Add_DS'),
    # url(r'^api-count/', views.CountPointsInPolygonView.as_view(), name='count'),
    # url(r'^api-dist/', views.AnalyzeAreaAroundPointView, name='distance'),
    url(r'^around-point/(?P<mappoint_id>[0-9]+)/$', templates.AroundPointView),
    url(r'^around-point/$', templates.AroundPointView),
]
