import os
import sys

from django.conf import settings
from django.shortcuts import get_object_or_404
from django_teams.models import TeamStatus
from rest_framework import views, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from project_share.models import (Application, ApplicationCategory,
                                  ApplicationDemo, ApplicationTheme,
                                  ExtendedUser, FileUpload, Goal, Project)
from rpi_csdt_community.serializers import (ApplicationCategorySerializer,
                                            ApplicationSerializer,
                                            ApplicationThemeSerializer,
                                            DemoSerializer, GoalSerializer,
                                            ProjectSerializer, TeamSerializer,
                                            UserSerializer)

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
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


class TeamViewSet(viewsets.ModelViewSet):
    model = TeamStatus
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = self.model.objects.select_related()
        user = self.request.query_params.get('user', None)
        queryset = queryset.filter(user=get_object_or_404(ExtendedUser, pk=user))
        queryset = queryset.filter(role='10') | queryset.filter(role='20')
        return queryset


class DemosViewSet(viewsets.ReadOnlyModelViewSet):
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


class GoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    lookup_field = 'application'

    def get_queryset(self):
        queryset = self.queryset
        application = self.request.query_params.get('application', None)
        if application is not None:
            queryset = queryset.filter(application__name=application)
        return queryset


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationCategory.objects.all()
    serializer_class = ApplicationCategorySerializer


class ApplicationThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationTheme.objects.all()
    serializer_class = ApplicationThemeSerializer


class FileUploadView(views.APIView):
    parser_class = (FileUploadParser,)
    model = FileUpload

    def put(self, request, format=None):
        file_object = request.data['file']
        file = FileUpload(file_path=file_object)
        file.save()
        path = os.path.join(settings.MEDIA_URL, file.file_path.url)
        return Response(status=201, data={'url': path, 'id': file.id})


class CurrentUserView(views.APIView):
    model = User

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Don't forgot to register your API in the rpi_csdt_community.urls!
