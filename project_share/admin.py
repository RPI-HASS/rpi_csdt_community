'''Project_Share Admin Setup'''

import os

import git

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from attachments.admin import AttachmentInlines
from project_share.models import Application, ApplicationDemo, ApplicationContext
from project_share.models import ApplicationTheme, ApplicationCategory
from project_share.models import Address
from project_share.models import Goal
from project_share.models import Classroom, Project, Approval, FileUpload
from project_share.models import ExtendedUser

from project_share.forms import ApplicationAdminForm

class ApplicationAdmin(admin.ModelAdmin):
    '''Adds save_model feature and get_form feature'''
    fields = ('name', 'url', 'description', 'application_type',
              'application_file', 'featured', 'categories', 'screenshot',)

    form = ApplicationAdminForm

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.save()
        obj.categories.clear()
        for category in form.cleaned_data['categories']:
            obj.categories.add(category)
        obj.save()
        git_file = git.Git(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        git_file.execute(["git", "submodule", "foreach", "git", "stash",])
        git_file.execute(["git", "submodule", "foreach", "git", "pull", "origin", "master"])
        git_file.execute(["python", "manage.py", "collectstatic", "--noinput"])

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['categories'].initial = obj.categories.all()
        return super(ApplicationAdmin, self).get_form(request, obj)

UserAdmin.list_display = ('username', 'email', 'gender', 'race', 'age', 'date_joined', 'is_staff')


class ClassListFilter(admin.SimpleListFilter):
    '''Filter for Class List'''
    title = _('Class')

    parameter_name = 'class'

    def value(self):
        class_value = super(ClassListFilter, self).value()
        if class_value is None:
            return 'mc'
        return class_value

    def lookups(self, request, model_admin):
        return (('mc', _('My class')), ('mca', ('Pending in my class')), ('ac', _('All classes')),)

    def queryset(self, request, queryset):
        if self.value() == 'mc':
            return queryset.filter(classroom__in=request.user.team_member.all())
        if self.value() == 'mca':
            return queryset.filter(classroom__in=request.user.team_member.all(), approved=False)
        else:
            return queryset

class ApprovalInline(admin.TabularInline):
    '''Sets model for TabularInLine to Approval'''
    model = Approval


class ProjectAdmin(admin.ModelAdmin):
    '''Sets up inlines for Admins'''
    inlines = [AttachmentInlines, ApprovalInline]
    list_filter = (ClassListFilter,)
    list_display = ('name', 'owner', 'application', 'classroom',
                    'approved', 'when_created', 'when_modified',)
    search_fields = ['owner__first_name', 'owner__last_name', 'name']

    def approve(self, request, queryset):
        '''Approval process for Admins'''
        Approval.objects.filter(project__in=queryset).update(approved_by=request.user)
        queryset.update(approved=True)

    approve.short_description = "Approve selected projects"
    actions = [approve]


class ApprovalAdmin(admin.ModelAdmin):
    '''Approval Placeholder'''
    pass


class ClassroomAdmin(admin.ModelAdmin):
    '''Students for each Teacher'''
    #exclude = ('teacher',)
    filter_horizontal = ('students',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ClassroomAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class GoalAdmin(admin.ModelAdmin):
    '''Admin for Goals'''
    list_display = ('name', 'application')
    list_filter = ('application',)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationContext)
admin.site.register(ApplicationDemo)
admin.site.register(ApplicationTheme)
admin.site.register(ApplicationCategory)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Address)
admin.site.register(Project, ProjectAdmin)
#admin.site.register(Approval, ApprovalAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(ExtendedUser, UserAdmin)
admin.site.register(FileUpload)
