import django

try:
    from django.db.models.loading import get_model
except ImportError:
    # Django 1.9 >
    from django.apps import apps
    get_model = apps.get_model
