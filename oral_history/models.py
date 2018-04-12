# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from filer.fields.image import FilerImageField

from filer.fields.file import FilerFileField

# Create your models here.

class Interview(models.Model):
    mp3_file = FilerFileField(related_name="oralhistory_mp3_file")
    pic = FilerImageField(null=True,blank=True, related_name="oralhistory_pic")
    full_name = models.TextField(max_length=60)
    date = models.CharField(blank=True, null=True, max_length=40)
    location = models.TextField(blank=True, null=True, max_length=70)
    interview_by = models.TextField(blank=True, null=True, max_length=60)
    birthplace = models.TextField(blank=True, null=True, max_length=60)
    occupation = models.TextField(blank=True, null=True, max_length=70)
    birth_year = models.TextField(blank=True, null=True, max_length=30)
    summary = models.TextField(blank=True, null=True, max_length=2000)
    slug = models.SlugField(unique=True)
    approved = models.BooleanField(default=False)


class OralHistories(models.Model):
    project_name = models.TextField(max_length=60)
    pic = FilerImageField(null=True,blank=True, related_name="oralhistory_pic")
    byline = models.TextField(blank=True, null=True, max_length=100)
    summary = models.TextField(blank=True, null=True, max_length=2000)
    about_html = models.TextField(blank=True, null=True, max_length=1000)
    url = models.CharField(max_length=70)
    slug = models.SlugField(unique=True)
    interviews = models.ManyToManyField(to=Interview, related_name="oralhistory_interviews")
