from rest_framework import serializers

from project_share.models import ApplicationDemo

class DemoSerializer(serializers.ModelSerializer):
    project_url = serializers.Field('zipfile.url')
    class Meta:
        model = ApplicationDemo
        fields = ('name', 'description', 'project_url')
