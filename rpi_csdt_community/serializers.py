from rest_framework import serializers

from project_share.models import ApplicationDemo, Project

class DemoSerializer(serializers.ModelSerializer):
    project_url = serializers.Field('zipfile.url')
    class Meta:
        model = ApplicationDemo
        fields = ('name', 'description', 'project_url')

class ProjectSerializer(serializers.ModelSerializer):
    project_url = serializers.Field('project.f.url')
    screenshot_url = serializers.Field('screenshot.f.url')

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'approved', 'application', 'owner', 'project_url', 'screenshot_url', 'project', 'screenshot')
        write_only_fields = ('project', 'screenshot')
        read_only_fields = ('id', 'approved',)
