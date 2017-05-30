"""Models for making, uploading, and owning projects and their owning applications."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django_comments.moderation import CommentModerator, moderator
from taggit.managers import TaggableManager


def application_application(instance, filename):
    """Create URL for getting to application."""
    return "applications/" + slugify(instance.name) + "." + slugify(filename.split('.')[-1])


def application_application_demo(instance, filename):
    """Create URL for getting to demo."""
    return "applications/demos/" + slugify(instance.application.__unicode__())\
           + "/" + slugify(filename.split('.')[:-1]) + "." + slugify(filename.split('.')[-1])


def application_application_goal(instance, filename):
    """Create URL for getting to goal."""
    return "applications/goals/" + slugify(instance.application.__unicode__())\
           + "/" + slugify(filename.split('.')[:-1]) + "." + slugify(filename.split('.')[-1])


def application_library(instance, filename):
    """Create URL for getting to library."""
    return "applications/libraries/" + slugify(filename.split('.')[:-1])\
           + "." + slugify(filename.split('.')[-1])


def project_project(instance, filename):
    """Create URL for getting to project."""
    return "applications/files/" + slugify(instance.owner.__unicode__()
                                           + '/' + '.'.join(filename.split('.')[:-1]))\
           + "." + slugify(filename.split('.')[-1])


def project_screenshot(instance, filename):
    """Create URL for getting to screenshot."""
    return "applications/screenshots/" + slugify(instance.owner.__unicode__()
                                                 + '/' + '.'.join(filename.split('.')[:-1]))\
           + "." + slugify(filename.split('.')[-1])


# These need to be removed someday; not removed now as it causes an error message
def module_module(instance, filename):
    """Create URL for getting to modules."""
    return "modules/" + slugify(instance.name) + "." + slugify(filename.split('.')[-1])


def module_library(instance, filename):
    """Create URL for getting to the module library."""
    return "modules/libraries/" + instance.name


class AutoDateTimeField(models.DateTimeField):
    """Save datetime field with time zone."""

    def pre_save(self, model_instance, add):
        return timezone.now()


class Classroom(models.Model):
    """This class has been deprecated for teams and should be removed."""

    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_classrooms')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_classrooms', blank=True)

    def __unicode__(self):
        return "%s's %s classroom" % (self.teacher, self.name)


class Approval(models.Model):
    """The object that determines whether a project is viewable to the public."""

    project = models.OneToOneField('Project')
    when_requested = AutoDateTimeField(default=timezone.now, null=True, blank=True)
    when_updated = AutoDateTimeField(default=timezone.now, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __unicode__(self):
        return "%s approval for %s" % (self.project.owner, self.project)


class Application(models.Model):
    """The base application for which all projects are based."""

    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    url = models.CharField(max_length=255, null=True, blank=True)
    codebase_url = models.CharField(max_length=255, null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)

    more_info_url = models.URLField(null=True, blank=True)

    application_type = models.CharField(max_length=5, choices=(
        ('CSNAP', 'cSnap'),
        ('BLOCK', 'Blockly/Scratch')))
    application_file = models.FileField(upload_to=application_application, null=True, blank=True)

    featured = models.BooleanField(default=True)
    screenshot = models.ImageField(upload_to="application_screenshot/", null=True)

    def get_context(self):
        """return all of the context data for the application."""
        ret = []
        for item in self.applicationcontext_set.filter(parent=None).order_by('order'):
            ret += [item]
            context = self._get_context(item)
            if context:
                ret += context
        return ret

    def _get_context(self, parent):
        """return all of the context data for the parent application."""
        ret = []
        for item in parent.applicationcontext_set.all().order_by('order'):
            ret += [item]
            context = self._get_context(item)
            if context:
                ret += context
        return ret

    def __unicode__(self):
        return self.name


class ApplicationContext(models.Model):
    """Has been deprecated in favor of CMS and should be removed."""

    application = models.ForeignKey('project_share.Application')
    parent = models.ForeignKey('project_share.ApplicationContext', null=True, blank=True)
    order = models.IntegerField(default=100)

    title = models.TextField()
    html_data = models.TextField(null=True, blank=True)

    def level(self):
        """Deprecated in favor of CMS and should be removed."""
        if self.parent is not None:
            return self.parent.level()+1
        return 1

    def __unicode__(self):
        return self.application.__unicode__() + "/" + self.title


class ApplicationDemo(models.Model):
    """Applications sometimes have demos that illustrate how they can be used."""

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey('project_share.Application')
    order = models.IntegerField(blank=True, default=1000)

    zipfile = models.FileField(upload_to=application_application_demo)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    """Projects are edited copies of applications owned by users."""

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    when_created = AutoDateTimeField(default=timezone.now, verbose_name="Created")
    when_modified = AutoDateTimeField(default=timezone.now, verbose_name="Last Changed")

    project = models.ForeignKey('project_share.FileUpload', null=True, blank=True, related_name='+')
    screenshot = models.ForeignKey('project_share.FileUpload', null=True, blank=True, related_name='+')
    classroom = models.ForeignKey('django_teams.Team', null=True, blank=True, related_name='+')

    tags = TaggableManager(blank=True)

    approved = models.BooleanField(default=False)

    parent = models.ForeignKey('project_share.Project', null=True, blank=True, related_name="children")

    @staticmethod
    def approved_projects():
        """Return a list of objects that have the approval of an admin for public display."""
        return Project.objects.filter(approved=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return the URL for this project."""
        return reverse('project-detail', kwargs={'pk': self.pk})


class Goal(models.Model):
    """In addition to demos, some applications have goals for what students should try and create."""

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application)

    thumbnail = models.FileField(upload_to=application_application_goal)
    image = models.FileField(upload_to=application_application_goal)

    def __unicode__(self):
        return self.name


class ExtendedUser(AbstractUser):
    """User has been expanded to collect gender, race, and age."""

    gender = models.CharField(max_length=100, null=True, blank=True)
    race = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.first_name != "":
            return "%s %s" % (self.first_name, self.last_name)
        return self.username


class FileUpload(models.Model):
    """All files uploaded by users for projects, principally screenshots, project data."""

    file_path = models.FileField(upload_to='files/%Y-%m-%d/')


class ProjectModerator(CommentModerator):
    """Should be replaced by msg being created by ryaholm."""

    moderate_after = -1


moderator.register(Project, ProjectModerator)


class Address(models.Model):
    """Information about where a student goes to school."""

    school = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255, verbose_name='State or Province')
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    teacher = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

    class Meta:
        verbose_name_plural = "Addresses"


class ApplicationTheme(models.Model):
    """Controls which categories are displayed, e.g. by cultures, or by CS content."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class ApplicationCategory(models.Model):
    """A category for sorting and displaying applications."""

    theme = models.ForeignKey('project_share.ApplicationTheme')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    applications = models.ManyToManyField('project_share.Application', related_name='categories', blank=True)

    def __unicode__(self):
        return self.name
