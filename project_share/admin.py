from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from attachments.admin import AttachmentInlines

from project_share.models import Application, ApplicationDemo, ApplicationType, Address, Project, Approval, FileUpload
from project_share.models import Classroom
from project_share.models import ExtendedUser

class ClassListFilter(admin.SimpleListFilter):
    title = _('Class')

    parameter_name = 'class'

    def value(self):
        t = super(ClassListFilter, self).value()
        if t == None:
            return 'mc'
        return t

    def lookups(self, request, model_admin):
        return (('mc', _('My class')), ('mca', ('Pending in my class')), ('ac', _('All classes')),)

    def queryset(self, request, queryset):
        if self.value() == 'mc':
            return queryset.filter(owner__student_classrooms__in=request.user.teacher_classrooms.all())
        if self.value() == 'mca':
            return queryset.filter(owner__student_classrooms__in=request.user.teacher_classrooms.all(), approved=False)
        else:
            return queryset

class ApprovalInline(admin.TabularInline):
    model = Approval
    
class ProjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines, ApprovalInline]
    list_filter = (ClassListFilter,)
    list_display = ('name', 'owner', 'application', 'approved',)
    search_fields = ['owner__first_name', 'owner__last_name', 'name']

    def approve(modeladmin, request, queryset):
       Approval.objects.filter(project__in=queryset).update(approved_by=request.user)
       queryset.update(approved=True)

    approve.short_description = "Approve selected projects"
    actions = [approve]

class ApprovalAdmin(admin.ModelAdmin):
    pass

class ClassroomAdmin(admin.ModelAdmin):
    #exclude = ('teacher',)
    filter_horizontal = ('students',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ClassroomAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Application)
admin.site.register(ApplicationDemo)
admin.site.register(ApplicationType)
admin.site.register(Address)
admin.site.register(Project, ProjectAdmin)
#admin.site.register(Approval, ApprovalAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(ExtendedUser, UserAdmin)
admin.site.register(FileUpload)
