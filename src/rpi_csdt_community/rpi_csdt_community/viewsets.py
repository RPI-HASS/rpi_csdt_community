from rest_framework import viewsets, routers

from project_share.models import Project, ApplicationDemo
from rpi_csdt_community.serializers import DemoSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    model = Project

class DemosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationDemo.objects.all()
    serializer_class = DemoSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.QUERY_PARAMS.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
        return queryset

# Don't forgot to register your API in the rpi_csdt_community.urls!
