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
    return "projects/files/" + instance.owner.__unicode__() + "/" + instance.name

def project_screenshot(instance, filename):
    return "projects/screenshots/" + instance.owner.__unicode__() + "/" + instance.name

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    APPLICATION_TYPES = (
        ("jaws", "Java Web Start"),
    )

    app_type = models.CharField(max_length=4, choices=APPLICATION_TYPES, default="jaws")
    file = models.FileField(upload_to=application_application)

    extensions = models.ManyToManyField('Application', null=True, blank=True)
    libraries = models.ManyToManyField('ApplicationLibrary', null=True, blank=True)

    def __unicode__(self):
        return self.name

class ApplicationParam(models.Model):
    application = models.ForeignKey(Application)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=4096)

    def __unicode__(self):
        return self.name

class ApplicationLibrary(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=10)

    LIBRARY_TYPES = (
        ('ext', 'Extension'),
        ('jar', 'Generic Jar'),
    )

    type = models.CharField(max_length=3, choices=LIBRARY_TYPES, default='extension')

    library = models.FileField(upload_to=application_library)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    project = models.FileField(upload_to=project_project)
    screenshot = models.FileField(upload_to=project_screenshot)

    tags = TaggableManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    class Meta:
        # Performance issue here?
        unique_together = (("name", "owner"),("project", "owner"),("screenshot", "owner"))

secretballot.enable_voting_on(Project)
