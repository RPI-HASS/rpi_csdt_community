from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django_pre_post.models import Attempt
from django_pre_post.serializers import AttemptSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class AttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    lookup_field = 'questionnaire'
    permission_classes = (IsAdminUser, )
