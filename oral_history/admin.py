# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import OralHistory, Interview, Tag

# Register your models here.

admin.site.register(OralHistory)
admin.site.register(Interview)
admin.site.register(Tag)
