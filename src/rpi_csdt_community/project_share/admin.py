from django.contrib import admin

from project_share.models import Application, ApplicationParam, Project

admin.site.register(Application)
admin.site.register(ApplicationParam)
admin.site.register(Project)
