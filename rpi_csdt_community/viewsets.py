'''RPI CSDT Community ViewSets'''

import os
import sys

from rest_framework import viewsets, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


from django_teams.models import TeamStatus
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    # from django.contrib.auth.models import User
    pass
else:
    USER = get_user_model()
from django.shortcuts import get_object_or_404


from project_share.models import Project, ApplicationDemo, \
    ExtendedUser, FileUpload, Goal, Application
from project_share.models import ApplicationTheme, ApplicationCategory

from .serializers import TeamSerializer, ProjectSerializer, GoalSerializer, \
    DemoSerializer, ApplicationSerializer, ApplicationCategorySerializer,\
    ApplicationThemeSerializer, UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Project View Set'''
    model = Project
    serializer_class = ProjectSerializer

    def get_object(self):
        obj = super(ProjectViewSet, self).get_object()
        if obj.owner is not None and obj.owner != self.request.user:
            original_pk = obj.pk
            obj.pk = None
            if original_pk is not None:
                sys.stdout.write("Updating parent")
                obj.parent = Project.objects.get(pk=original_pk)
        # If this project is published, create a new one by resetting pk
        if obj.approved:
            obj.pk = None
            obj.approved = False
        obj.owner = self.request.user
        return obj

    def get_queryset(self):
        queryset = self.model.objects.all()
        user = self.request.query_params.get('owner', None)
        if user is not None:
            queryset = queryset.filter(owner=get_object_or_404(ExtendedUser, pk=user))
        return queryset


class TeamViewSet(viewsets.ModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Team View Set'''
    model = TeamStatus
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = self.model.objects.select_related()
        user = self.request.query_params.get('user', None)
        queryset = queryset.filter(user=get_object_or_404(ExtendedUser, pk=user))
        queryset = queryset.filter(role='10') | queryset.filter(role='20')
        return queryset


class DemosViewSet(viewsets.ReadOnlyModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Demo View Set'''
    queryset = ApplicationDemo.objects.all()
    serializer_class = DemoSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.query_params.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
        queryset = queryset.order_by('order')
        return queryset


class GoalViewSet(viewsets.ReadOnlyModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Goal View Set'''
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.query_params.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
        return queryset


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Application View Set'''
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = 'name'


class ApplicationCategoryViewSet(viewsets.ReadOnlyModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Application Category View Set'''
    queryset = ApplicationCategory.objects.all()
    serializer_class = ApplicationCategorySerializer


class ApplicationThemeViewSet(viewsets.ReadOnlyModelViewSet):  \
        # pylint: disable=too-many-ancestors
    '''Application Theme View Set'''
    queryset = ApplicationTheme.objects.all()
    serializer_class = ApplicationThemeSerializer


class FileUploadView(views.APIView):
    '''File Upload View'''
    parser_class = (FileUploadParser,)
    model = FileUpload

    # pylint: disable=R0201
    def put(self, request):
        '''Uploads file to Database'''
        file_object = request.data['file']
        file_to_upload = FileUpload(f=file_object)
        file_to_upload.save()
        path = os.path.join(settings.MEDIA_URL, file_to_upload.f.url)
        return Response(status=201, data={'url': path, 'id': file_to_upload.id})


class CurrentUserView(views.APIView):
    '''Current User View'''
    model = USER

    def get(self, request):
        '''Serializer for Current User View'''
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Don't forgot to register your API in the rpi_csdt_community.urls!
