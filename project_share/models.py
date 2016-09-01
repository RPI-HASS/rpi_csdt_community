from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django_comments.moderation import CommentModerator, moderator
from taggit.models import TaggedItemBase, GenericTaggedItemBase
from django_teams.models import Team

import secretballot
import json
import zipfile as zippy

from taggit.managers import TaggableManager

def application_application(instance, filename):
    return "applications/" + slugify(instance.name) + "." + slugify(filename.split('.')[-1])

def application_application_demo(instance, filename):
    return "applications/demos/" + slugify(instance.application.__unicode__()) + "/" + slugify(filename.split('.')[:-1]) + "." + slugify(filename.split('.')[-1])

def application_application_goal(instance, filename):
    return "applications/goals/" + slugify(instance.application.__unicode__()) + "/" + slugify(filename.split('.')[:-1]) + "." + slugify(filename.split('.')[-1])

def application_library(instance, filename):
    return "applications/libraries/" + slugify(filename.split('.')[:-1]) + "." + slugify(filename.split('.')[-1])

def project_project(instance, filename):
    return "applications/files/" + slugify(instance.owner.__unicode__() + '/' + '.'.join(filename.split('.')[:-1])) + "." + slugify(filename.split('.')[-1])

def project_screenshot(instance, filename):
    return "applications/screenshots/" + slugify(instance.owner.__unicode__() + '/' + '.'.join(filename.split('.')[:-1])) + "." + slugify(filename.split('.')[-1])

# These need to be removed someday; not removed now as it causes an error message
def module_module(instance, filename):
    return "modules/" + slugify(instance.name) + "." + slugify(filename.split('.')[-1])

def module_library(instance, filename):
    return "modules/libraries/" + instance.name

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_classrooms')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_classrooms', blank=True)

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

    url = models.CharField(max_length=255, null=True, blank=True)
    codebase_url = models.CharField(max_length=255, null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)

    more_info_url = models.URLField(null=True, blank=True)

    application_type = models.CharField(max_length=5, choices= (
            ('CSNAP', 'cSnap'),
            ('BLOCK', 'Blockly/Scratch'),
        ))
    application_file = models.FileField(upload_to=application_application, null=True, blank=True)

    featured = models.BooleanField(default=True)
    screenshot = models.ImageField(upload_to="application_screenshot/", null=True)

    def get_context(self):
        # Returns all context data ordered
        ret = []
        for item in self.applicationcontext_set.filter(parent=None).order_by('order'):
            ret += [item]
            l = self._get_context(item)
            if len(l) > 0:
                ret += l
        return ret

    def _get_context(self, parent):
        ret = []
        for item in parent.applicationcontext_set.all().order_by('order'):
            ret += [item]
            l = self._get_context(item)
            if len(l) > 0:
                ret += l
        return ret

    def __unicode__(self):
        return self.name

class ApplicationContext(models.Model):
    application = models.ForeignKey('project_share.Application')
    parent = models.ForeignKey('project_share.ApplicationContext', null=True, blank=True)
    order = models.IntegerField(default=100)

    title = models.TextField()
    html_data = models.TextField(null=True, blank=True)

    def level(self):
        if self.parent != None:
            return self.parent.level()+1
        return 1

    def __unicode__(self):
        return self.application.__unicode__() + "/" + self.title

class ApplicationDemo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey('project_share.Application')
    order = models.IntegerField(blank=True, default=1000)

    zipfile = models.FileField(upload_to=application_application_demo)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    project = models.ForeignKey('project_share.FileUpload', null=True, blank=True, related_name='+')
    screenshot = models.ForeignKey('project_share.FileUpload', null=True, blank=True, related_name='+')
    classroom = models.ForeignKey('django_teams.Team', null=True, blank=True, related_name='+')

    tags = TaggableManager(blank=True)

    approved = models.BooleanField(default=False)

    parent = models.ForeignKey('project_share.Project', null=True, blank=True, related_name="children")

    @staticmethod
    def approved_projects():
        return Project.objects.filter(approved=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

class Goal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)

    thumbnail = models.FileField(upload_to=application_application_goal)
    image = models.FileField(upload_to=application_application_goal)

    def __unicode__(self):
        return self.name

class ExtendedUser(AbstractUser):
    gender = models.CharField(max_length=100, null=True, blank=True)
    race = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    def __unicode__(self):
        if self.first_name != "":
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

class FileUpload(models.Model):
    f = models.FileField(upload_to='files/%Y-%m-%d/')

class ProjectModerator(CommentModerator):
    moderate_after = -1

moderator.register(Project, ProjectModerator)

class Address(models.Model):
    school = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255, verbose_name = 'State or Province')
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    teacher = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

    class Meta:
      verbose_name_plural = "Addresses"

class ApplicationTheme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class ApplicationCategory(models.Model):
    theme = models.ForeignKey('project_share.ApplicationTheme')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    applications = models.ManyToManyField('project_share.Application', related_name='categories', blank=True)

    def __unicode__(self):
        return self.name

import project_share.signals
