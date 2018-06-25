# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import OralHistory, Interview, Tag

# Register your models here.


def approve_tags(modeladmin, request, queryset):
    queryset.update(approved=True)


def approve_interviews(modeladmin, request, queryset):
    queryset.update(approved=True)


def approve_ohps(modeladmin, request, queryset):
    queryset.update(approved=True)


def deapprove_tags(modeladmin, request, queryset):
    queryset.update(approved=False)


def deapprove_interviews(modeladmin, request, queryset):
    queryset.update(approved=False)


def deapprove_ohps(modeladmin, request, queryset):
    queryset.update(approved=False)


approve_tags.short_description = "Approve selected tags"
approve_interviews.short_description = "Approve selected interviews"
approve_ohps.short_description = "Approve selected OHPs"
deapprove_tags.short_description = "De-approve selected tags"
deapprove_interviews.short_description = "De-approve selected interviews"
deapprove_ohps.short_description = "De-approve selected OHPs"


class TagAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'approved',)
    actions = [approve_tags, deapprove_tags]


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'approved',)
    actions = [approve_interviews, deapprove_interviews]


class OHPAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_official', 'approved',)
    actions = [approve_ohps, deapprove_ohps]


admin.site.register(OralHistory, OHPAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Tag, TagAdmin)
