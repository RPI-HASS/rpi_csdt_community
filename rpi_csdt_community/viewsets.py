from rest_framework import viewsets, routers, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from project_share.models import Project, ApplicationDemo, ExtendedUser, FileUpload, Goal
from rpi_csdt_community.serializers import DemoSerializer, GoalSerializer, ProjectSerializer, UserSerializer
from django.conf import settings
import os
import sys

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer

    def pre_save(self, obj):
        super(ProjectViewSet, self).pre_save(obj)
        if obj.owner != None and obj.owner != self.request.user:
            original_pk = obj.pk
            obj.pk = None
            if original_pk != None:
                sys.stdout.write("Updating parent")
                obj.parent = Project.objects.get(pk=original_pk)
            obj.save()
        obj.owner = self.request.user

    def get_queryset(self):
        queryset = self.model.objects.all()
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

class GoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.QUERY_PARAMS.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
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

class CurrentUserView(views.APIView):
    model = User
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Don't forgot to register your API in the rpi_csdt_community.urls!
