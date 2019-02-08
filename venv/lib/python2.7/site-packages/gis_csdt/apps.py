from django.apps import AppConfig


class GISAppConfig(AppConfig):
    name = 'gis_csdt'

    def ready(self):
        from gis_csdt import signals
