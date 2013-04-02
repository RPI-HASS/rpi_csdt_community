from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from taggit.managers import TaggableManager

def application_application(instance, filename):
    return "applications/" + filename

def project_project(instance, filename):
    return "projects/files/" + instance.owner.__unicode__() + "/" + instance.name

def project_screenshot(instance, filename):
    return "projects/screenshots/" + instance.owner.__unicode__() + "/" + instance.name

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    APPLICATION_TYPES = (
        ("jaws", "Java Web Start"),
    )

    app_type = models.CharField(max_length=4, choices=APPLICATION_TYPES, default="jaws")
    application = models.FileField(upload_to=application_application)

    def __unicode__(self):
        return self.name

class ApplicationParam(models.Model):
    application = models.ForeignKey(Application)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=4096)

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
