from __future__ import unicode_literals

from django.db import models

from project_share.models import Application

# Create your models here.

class Entry(models.Model):
    name = models.CharField(max_length=255)
    application = models.ForeignKey(Application, related_name="guide_entry_app")
    link = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, default="")

    def __unicode__(self):
        return "{}".format(self.name)
