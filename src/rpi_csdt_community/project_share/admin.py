from django.contrib import admin
from attachments.admin import AttachmentInlines

from project_share.models import Application, Project

class ProjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

admin.site.register(Application)
admin.site.register(Project, ProjectAdmin)
