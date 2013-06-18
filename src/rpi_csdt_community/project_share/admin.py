from django.contrib import admin

from project_share.models import Application, ApplicationParam, ApplicationLibrary, Project

admin.site.register(Application)
admin.site.register(ApplicationParam)
admin.site.register(ApplicationLibrary)
admin.site.register(Project)
