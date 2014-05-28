from rest_framework import serializers

from project_share.models import ApplicationDemo, Project

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class DemoSerializer(serializers.ModelSerializer):
    project_url = serializers.Field('zipfile.url')
    class Meta:
        model = ApplicationDemo
        fields = ('id', 'name', 'description', 'project_url')

class ProjectSerializer(serializers.ModelSerializer):
    project_url = serializers.Field('project.f.url')
    screenshot_url = serializers.Field('screenshot.f.url')

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'approved', 'application', 'owner', 'project_url', 'screenshot_url', 'project', 'screenshot')
        write_only_fields = ('project', 'screenshot')
        read_only_fields = ('id', 'approved','owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'first_name', 'last_name')
