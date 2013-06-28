from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from taggit.models import TaggedItemBase, GenericTaggedItemBase

import secretballot

from taggit.managers import TaggableManager

def application_application(instance, filename):
    return slugify("applications/" + filename)

def application_library(instance, filename):
    return slugify("applications/libraries/" + filename)

def project_project(instance, filename):
    return slugify("projects/files/" + instance.owner.__unicode__() + "/" + instance.name + ".xml")

def project_screenshot(instance, filename):
    return slugify("projects/screenshots/" + instance.owner.__unicode__() + "/" + instance.name)

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_classrooms')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_classrooms', null=True, blank=True)

    def __unicode__(self):
        return "%s's %s classroom" % (self.teacher, self.name)

class Approval(models.Model):
    project = models.OneToOneField('Project')
    when_requested = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __unicode__(self):
        return "%s approval for %s" % (self.project.owner, self.project)

class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    url = models.CharField(max_length=255)
    codebase_url = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ProjectManager(models.Manager):
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(approved=True)

class TaggedObjectManager(models.Manager):
    def get_query_set(self):
        return super(TaggedObjectManager, self).get_query_set().filter(content_object__approved=True)

class TaggedProject(GenericTaggedItemBase):
    objects = TaggedObjectManager()

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    project = models.FileField(upload_to=project_project)
    screenshot = models.FileField(upload_to=project_screenshot)

    tags = TaggableManager(blank=True)

    approved = models.BooleanField(default=False)

    objects = models.Manager()
    approved_objects = ProjectManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk})

    class Meta:
        # Performance issue here?
        unique_together = (("name", "owner"),("project", "owner"),("screenshot", "owner"))

class ExtendedUser(AbstractUser):
    def __unicode__(self):
        if self.first_name != "":   
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

secretballot.enable_voting_on(Project, base_manager=ProjectManager)

import project_share.signals
