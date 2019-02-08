"""Serialize the models from projectshare into displayable items for admin / forms."""
from rest_framework import serializers
from django_pre_post.models import Attempt, Questionnaire
from django.contrib.auth import get_user_model
User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    """Display the filled out questionnaires"""

    class Meta:
        model = User
        fields = ('username',)


class QuestionnaireSerializer(serializers.ModelSerializer):
    """Display the filled out questionnaires"""
    owner = OwnerSerializer()

    class Meta:
        model = Questionnaire
        fields = ('name', 'owner')


class AttemptSerializer(serializers.ModelSerializer):
    """Display the filled out questionnaires"""
    questionnaire = QuestionnaireSerializer()
    owner = OwnerSerializer()
    answers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Attempt
        fields = ('questionnaire', 'owner', 'created', 'answers')
