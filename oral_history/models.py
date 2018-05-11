# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.db import models
from django.template.defaultfilters import slugify

from filer.fields.image import FilerImageField

from project_share.models import Project

User = get_user_model()

# Create your models here.


def my_awesome_upload_function(instance, filename):
    return os.path.join('oralhistoryproject/%s/' % instance.id, filename)


class Interview(models.Model):
    project = models.ForeignKey('OralHistory')
    mp3_file = models.FileField(blank=True,
                                null=True,
                                validators=[FileExtensionValidator(['mp3'])],
                                upload_to='oralhistoryproject/%Y-%m-%d/')
    pic = models.ImageField(null=True, blank=True,
                            validators=[validate_image_file_extension],
                            upload_to='oralhistoryproject/%Y-%m-%d/')
    full_name = models.TextField(max_length=60)
    date = models.CharField(blank=True, null=True, max_length=40)
    location = models.TextField(blank=True, null=True, max_length=70)
    interview_by = models.TextField(blank=True, null=True, max_length=60)
    birthplace = models.TextField(blank=True, null=True, max_length=60)
    occupation = models.TextField(blank=True, null=True, max_length=70)
    birth_year = models.TextField(blank=True, null=True, max_length=30)
    summary = models.TextField(blank=True, null=True, max_length=45000)
    slug = models.SlugField(unique=True, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)
    csdt_project = models.ForeignKey('project_share.Project', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(Interview, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.approved:
            status = ""
        else:
            status = "NOT_APPROVED"
        try:
            username = self.user.username or 'null'
        except AttributeError:
            username = 'null'
        return self.project.project_name + " => " + self.full_name + " by " + username + " " + status


class OralHistory(models.Model):
    project_name = models.TextField(max_length=60, unique=True)
    pic = models.ImageField(null=True, blank=True,
                            validators=[validate_image_file_extension],
                            upload_to='oralhistoryproject/%Y-%m-%d/')
    byline = models.TextField(blank=True, null=True, max_length=100)
    summary = models.TextField(blank=True, null=True, max_length=2000)
    about_html = models.TextField(blank=True, null=True, max_length=1000)
    slug = models.SlugField(unique=True, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    is_official = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        try:
            username = self.user.username
        except AttributeError:
            username = 'null'
        return "Project: " + self.project_name + " by " + username


class Tag(models.Model):
    timestamp = models.IntegerField()
    tag = models.CharField(max_length=40)
    interview = models.ForeignKey('Interview', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return "Tag: " + self.interview.project.project_name + \
            ": " + self.interview.full_name + " => \"" + self.tag + \
            "\", " + str(self.timestamp) + " secs"

    def to_timestamp(self):
        hours = int(self.timestamp / 3600)
        if hours > 0:
            mins = int((self.timestamp - (hours * 3600)) / 60)
        else:
            mins = int(self.timestamp / 60)
        secs = self.timestamp % 60
        if hours > 0:
            return "{}:{}:{}".format(str(hours).zfill(2), str(mins).zfill(2), str(secs).zfill(2))
        else:
            return "{}:{}".format(str(mins).zfill(2), str(secs).zfill(2))
