from rest_framework import serializers

from project_share.models import ApplicationDemo, Project, Goal, Application
from project_share.models import ApplicationTheme, ApplicationCategory

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class DemoSerializer(serializers.ModelSerializer):
    project_url = serializers.URLField(source='zipfile.url', read_only=True)
    class Meta:
        model = ApplicationDemo
        fields = ('id', 'name', 'description', 'project_url')

class GoalSerializer(serializers.ModelSerializer):
    thumb_url = serializers.URLField(source='thumbnail.url', read_only=True)
    img_url = serializers.URLField(source='image.url', read_only=True)

    class Meta:
        model = Goal
        fields = ('description', 'name', 'thumb_url', 'img_url')

class ProjectSerializer(serializers.ModelSerializer):
    project_url = serializers.URLField(source='project.f.url', read_only=True)
    screenshot_url = serializers.URLField(source='screenshot.f.url', read_only=True)

    def __init__(self, *args, **kwargs):
        super(ProjectSerializer, self).__init__(*args, **kwargs)
        self.request = kwargs['context']['request']

    def create(self, validated_data):
        validated_data['owner'] = self.request.user
        return super(ProjectSerializer, self).create(validated_data)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'approved', 'application', 'owner', 'project_url', 'screenshot_url', 'project', 'screenshot',)
        write_only_fields = ('project', 'screenshot',)
        read_only_fields = ('id', 'approved','owner', 'project_url', 'screenshot_url',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'first_name', 'last_name')

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'version', 'description', 'url', 'application_file', 'featured', 'application_type', 'categories', 'screenshot')

class ApplicationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationCategory

class ApplicationThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationTheme
