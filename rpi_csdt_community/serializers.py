'''Serializers for Community Webpage'''

from rest_framework import serializers

from project_share.models import ApplicationDemo, Project, Goal, Application
from project_share.models import ApplicationTheme, ApplicationCategory
from django_teams.models import TeamStatus

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    USER = get_user_model()


class DemoSerializer(serializers.ModelSerializer):
    '''Demo Serializer'''
    project_url = serializers.URLField(source='zipfile.url', read_only=True)
    class Meta:
        model = ApplicationDemo
        fields = ('id', 'name', 'description', 'project_url')

class GoalSerializer(serializers.ModelSerializer):
    '''Goal Serializer'''
    thumb_url = serializers.URLField(source='thumbnail.url', read_only=True)
    img_url = serializers.URLField(source='image.url', read_only=True)

    class Meta:
        model = Goal
        fields = ('description', 'name', 'thumb_url', 'img_url')

class ProjectSerializer(serializers.ModelSerializer):
    '''Project Serializer'''
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
        fields = ('id', 'name', 'description', 'classroom',
                  'approved', 'application', 'owner', 'project_url',
                  'screenshot_url', 'project', 'screenshot',)
        write_only_fields = ('project', 'screenshot',)
        read_only_fields = ('id', 'approved', 'owner', 'project_url', 'screenshot_url',)

class TeamSerializer(serializers.ModelSerializer):
    '''Team Serializer'''
    team_name = serializers.StringRelatedField(source='team', read_only=True)

    def __init__(self, *args, **kwargs):
        super(TeamSerializer, self).__init__(*args, **kwargs)
        self.request = kwargs['context']['request']

    def create(self, validated_data):
        validated_data['owner'] = self.request.user
        return super(TeamSerializer, self).create(validated_data)

    class Meta:
        model = TeamStatus
        fields = ('id', 'role', 'team_name', 'team')
        read_only_fields = ('id', 'role', 'team_name', 'team')


class UserSerializer(serializers.ModelSerializer):
    '''User Serializer'''
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'first_name', 'last_name')

class ApplicationSerializer(serializers.ModelSerializer):
    '''Application Serializer'''
    class Meta:
        model = Application
        fields = ('id', 'name', 'version', 'description', 'url', 'application_file',
                  'featured', 'application_type', 'categories', 'screenshot')

class ApplicationCategorySerializer(serializers.ModelSerializer):
    '''Application Category Serializer'''
    class Meta:
        model = ApplicationCategory

class ApplicationThemeSerializer(serializers.ModelSerializer):
    '''Application Theme Serializer'''
    class Meta:
        model = ApplicationTheme
