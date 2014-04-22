from rest_framework import viewsets, routers, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from project_share.models import Project, ApplicationDemo, ExtendedUser, FileUpload
from rpi_csdt_community.serializers import DemoSerializer, ProjectSerializer
from django.conf import settings
import os

class ProjectViewSet(viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super(ProjectViewSet, self).get_queryset()
        user = self.request.QUERY_PARAMS.get('owner', None)
        if user is not None:
          queryset = queryset.filter(owner=get_object_or_404(ExtendedUser, pk=user))
        return queryset

class DemosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationDemo.objects.all()
    serializer_class = DemoSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.QUERY_PARAMS.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
        queryset = queryset.order_by('order')
        return queryset

class FileUploadView(views.APIView):
    parser_class = (FileUploadParser,)
    model = FileUpload

    def post(self, request, format=None):
        file_object = request.FILES['file']
        f = FileUpload(f=file_object)
        f.save()
        path = os.path.join(settings.MEDIA_URL, f.f.url)
        return Response(status=201, data={'url':path, 'id':f.id})

# Don't forgot to register your API in the rpi_csdt_community.urls!
