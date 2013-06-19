from django.contrib import admin
from attachments.admin import AttachmentInlines

from project_share.models import Application, ApplicationParam, ApplicationLibrary, Project

class ProjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

admin.site.register(Application)
admin.site.register(ApplicationParam)
admin.site.register(ApplicationLibrary)
admin.site.register(Project, ProjectAdmin)
