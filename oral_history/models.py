# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.db import models
from django.template.defaultfilters import slugify



from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

# Create your models here.

def my_awesome_upload_function(instance, filename):
    return os.path.join('oralhistoryproject/%s/' % instance.id, filename)

class Interview(models.Model):
    project = models.ForeignKey('OralHistory')
    mp3_file = models.FileField(blank=True,
                       null=True,
                       validators=[FileExtensionValidator(['mp3'])],
                       upload_to=my_awesome_upload_function)
    pic = models.ImageField(null=True, blank=True, validators=[validate_image_file_extension], upload_to=my_awesome_upload_function)
    full_name = models.TextField(max_length=60)
    date = models.CharField(blank=True, null=True, max_length=40)
    location = models.TextField(blank=True, null=True, max_length=70)
    interview_by = models.TextField(blank=True, null=True, max_length=60)
    birthplace = models.TextField(blank=True, null=True, max_length=60)
    occupation = models.TextField(blank=True, null=True, max_length=70)
    birth_year = models.TextField(blank=True, null=True, max_length=30)
    summary = models.TextField(blank=True, null=True, max_length=15000)
    slug = models.SlugField(unique=True, blank=False, null=False)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(Interview, self).save(*args, **kwargs)


    def __unicode__(self):
        return "Interview: " + self.project.project_name + "=> " + self.full_name


class OralHistory(models.Model):
    project_name = models.TextField(max_length=60, unique=True)
    pic = FilerImageField(null=True,blank=True, related_name="oralhistory_pic")
    byline = models.TextField(blank=True, null=True, max_length=100)
    summary = models.TextField(blank=True, null=True, max_length=2000)
    about_html = models.TextField(blank=True, null=True, max_length=1000)
    url = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=False, null=False)

    def __unicode__(self):
        return "Project: " + self.project_name


class Tag(models.Model):
    timestamp = models.IntegerField()
    tag = models.CharField(max_length=40)
    interview = models.ForeignKey('Interview', on_delete=models.CASCADE)

    def __unicode__(self):
        return "Tag: " + self.interview.project.project_name + ": " + self.interview.full_name + "=> " + self.tag + " (" + self.timestamp + ")secs"
