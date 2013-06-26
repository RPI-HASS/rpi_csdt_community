from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

import secretballot

from taggit.managers import TaggableManager

def application_application(instance, filename):
    return "applications/" + filename

def application_library(instance, filename):
    return "applications/libraries/" + filename

def project_project(instance, filename):
    return "projects/files/" + instance.owner.__unicode__() + "/" + instance.name + ".xml"

def project_screenshot(instance, filename):
    return "projects/screenshots/" + instance.owner.__unicode__() + "/" + instance.name

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    url = models.CharField(max_length=255)
    codebase_url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    project = models.FileField(upload_to=project_project)
    screenshot = models.FileField(upload_to=project_screenshot)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    class Meta:
        # Performance issue here?
        unique_together = (("name", "owner"),("project", "owner"),("screenshot", "owner"))

secretballot.enable_voting_on(Project)
