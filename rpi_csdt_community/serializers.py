"""Serialize the models from projectshare into displayable items for admin / forms."""
from django_teams.models import TeamStatus
from rest_framework import serializers

from project_share.models import (Application, ApplicationCategory,
                                  ApplicationDemo, ApplicationTheme, Goal,
                                  Project)

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class DemoSerializer(serializers.ModelSerializer):
    """Display the id, name, description, and url for the demo."""

    project_url = serializers.URLField(source='zipfile.url', read_only=True)

    class Meta:
        model = ApplicationDemo
        fields = ('id', 'name', 'description', 'project_url')


class GoalSerializer(serializers.ModelSerializer):
    """Display the name, description, and urls for the goal."""

    thumb_url = serializers.URLField(source='thumbnail.url', read_only=True)
    img_url = serializers.URLField(source='image.url', read_only=True)

    class Meta:
        model = Goal
        fields = ('description', 'name', 'thumb_url', 'img_url')


class ProjectSerializer(serializers.ModelSerializer):
    """Validate changes and limit access, aswell as specify display for project."""

    project_url = serializers.URLField(source='project.file_path.url', read_only=True)
    screenshot_url = serializers.URLField(source='screenshot.file_path.url', read_only=True)

    def __init__(self, *args, **kwargs):
        """Set the context."""
        super(ProjectSerializer, self).__init__(*args, **kwargs)
        self.request = kwargs['context']['request']

    def create(self, validated_data):
        """Validate owner."""
        validated_data['owner'] = self.request.user
        return super(ProjectSerializer, self).create(validated_data)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'classroom', 'approved', 'application', 'owner', 'project_url',
                  'screenshot_url', 'project', 'screenshot')
        write_only_fields = ('project', 'screenshot')
        read_only_fields = ('id', 'approved', 'owner', 'project_url', 'screenshot_url')


class TeamSerializer(serializers.ModelSerializer):
    """Validate changes and limit access, aswell as specify display for team."""

    team_name = serializers.StringRelatedField(source='team', read_only=True)

    def __init__(self, *args, **kwargs):
        """Set the context."""
        super(TeamSerializer, self).__init__(*args, **kwargs)
        self.request = kwargs['context']['request']

    def create(self, validated_data):
        """Validate owner."""
        validated_data['owner'] = self.request.user
        return super(TeamSerializer, self).create(validated_data)

    class Meta:
        model = TeamStatus
        fields = ('id', 'role', 'team_name', 'team')
        read_only_fields = ('id', 'role', 'team_name', 'team')


class UserSerializer(serializers.ModelSerializer):
    """All fields are read only for users."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'first_name', 'last_name')


class ApplicationSerializer(serializers.ModelSerializer):
    """Display everything for the application."""

    class Meta:
        model = Application
        fields = ('id', 'name', 'version', 'description', 'url', 'application_file', 'featured', 'rank',
                  'application_type', 'categories', 'screenshot')


class ApplicationCategorySerializer(serializers.ModelSerializer):
    """Stub for displaying category."""

    class Meta:
        model = ApplicationCategory
        fields = ('id', 'theme', 'name', 'description', 'applications')


class ApplicationThemeSerializer(serializers.ModelSerializer):
    """Stub for displaying theme."""

    class Meta:
        model = ApplicationTheme
        fields = ('id', 'name', 'description')
