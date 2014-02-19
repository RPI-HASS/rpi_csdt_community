from rest_framework import serializers

from project_share.models import ApplicationDemo

class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDemo
        fields = ('name', 'description', 'zipfile')
