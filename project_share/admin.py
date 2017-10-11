"""Admin models and settings for the projects, applications, and approvals."""
from attachments.admin import AttachmentInlines
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from project_share.forms import ApplicationAdminForm
from project_share.models import (Address, Application, ApplicationCategory,
                                  ApplicationContext, ApplicationDemo,
                                  ApplicationTheme, Approval, Classroom,
                                  ExtendedUser, FileUpload, Goal, Project,
                                  ExtensionOrder, Extension)


class ExtensionOrderInline(admin.TabularInline):
    model = ExtensionOrder
    extra = 1

class ExtensionAdmin(admin.ModelAdmin):
    """Enable filters for classrooms and sets the display for projects."""

    list_display = ('name', 'path')


class ApplicationAdmin(admin.ModelAdmin):
    """Innumerate application updating from admin."""

    fields = ('name', 'url', 'description', 'application_type', 'application_file', 'featured', 'categories',
              'screenshot', 'rankApp')

    form = ApplicationAdminForm
    inlines = (ExtensionOrderInline,)

    def save_model(self, request, obj, form, change):
        """Update submodules when applications are updated."""
        if obj.id is None:
            obj.save()
        obj.categories.clear()
        for category in form.cleaned_data['categories']:
            obj.categories.add(category)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        """Include categories in form."""
        if obj:
            self.form.base_fields['categories'].initial = obj.categories.all()
        return super(ApplicationAdmin, self).get_form(request, obj)


UserAdmin.list_display = ('username', 'email', 'gender', 'race', 'age', 'date_joined', 'is_staff')


class ClassListFilter(admin.SimpleListFilter):
    """A filter used by projects to get by specific classrooms."""

    title = _('Class')
    parameter_name = 'class'

    def value(self):
        """Return whether it is filtering by my class, pending in my class, and all classes."""
        filt = super(ClassListFilter, self).value()
        if filt is None:
            return 'mc'
        return filt

    def lookups(self, request, model_admin):
        """The three ways that the filter filters."""
        return (('mc', _('My class')), ('mca', ('Pending in my class')), ('ac', _('All classes')),)

    def queryset(self, request, queryset):
        """The actual filter as applied to queryset."""
        if self.value() == 'mc':
            return queryset.filter(classroom__in=request.user.team_member.all())
        if self.value() == 'mca':
            return queryset.filter(classroom__in=request.user.team_member.all(), approved=False)
        else:
            return queryset


class ApprovalInline(admin.TabularInline):
    """Just displays approvals."""

    model = Approval


class ProjectAdmin(admin.ModelAdmin):
    """Enable filters for classrooms and sets the display for projects."""

    inlines = [AttachmentInlines, ApprovalInline]
    list_filter = (ClassListFilter,)
    list_display = ('name', 'owner', 'application', 'classroom', 'approved', 'when_created', 'when_modified',)
    search_fields = ['owner__first_name', 'owner__last_name', 'name']

    def approve(modeladmin, request, queryset):
        """Change to filter by approval."""
        Approval.objects.filter(project__in=queryset).update(approved_by=request.user)
        queryset.update(approved=True)

    approve.short_description = "Approve selected projects."
    actions = [approve]


class ApprovalAdmin(admin.ModelAdmin):
    """Display nothing for approvals."""

    pass


class ClassroomAdmin(admin.ModelAdmin):
    """Deprecated, should be removed."""

    # exclude = ('teacher',)
    filter_horizontal = ('students',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Deprecated, should be removed."""
        if db_field.name == 'teacher':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ClassroomAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class GoalAdmin(admin.ModelAdmin):
    """Goals merely need to display name and app."""

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
# admin.site.register(Approval, ApprovalAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(ExtendedUser, UserAdmin)
admin.site.register(FileUpload)
admin.site.register(Extension, ExtensionAdmin)
