'''Project_Share views.py'''

from django_teams.models import Ownership
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import USER
else:
    USER = get_user_model()

from taggit.models import Tag

from extra_views import SortableListMixin
from extra_views import SearchableListMixin

from project_share.models import Application, Project, ApplicationDemo, Approval, Address
from project_share.forms import ProjectForm, ApprovalForm, AddressForm, ProjectUnpublishForm


class RestrictPermissionMixin(object):
    '''Mixin'''
    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        self.kwargs = kwargs
        self.request = request
        return super(RestrictPermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        '''Returns object'''
        if hasattr(self, 'object'):
            return self.object
        object_to_return = super(RestrictPermissionMixin, self).get_object()

        # If the object doesn't belong to this user and isn't published, throw a error 403
        if (not object_to_return.approved and
                object_to_return.owner != self.request.user) \
                and not self.request.user.is_superuser:
            raise PermissionDenied()
        self.object = object_to_return
        return object_to_return


class ApplicationList(ListView):  # pylint: disable=too-many-ancestors
    '''Application List View'''
    model = Application


class ApplicationDetail(DetailView):  # pylint: disable=too-many-ancestors
    '''Application Detail View'''
    model = Application


class ApplicationRunDetail(DetailView):  # pylint: disable=too-many-ancestors
    '''Application Run Detail View'''
    model = Application
    context_object_name = 'application'

    def render_to_response(self, context, **response_kwargs):
        try:
            context['GOOGLE_ANALYTICS_PROPERTY_ID'] = settings.GOOGLE_ANALYTICS_PROPERTY_ID
        except:
            pass
        return super(ApplicationRunDetail, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return ['project_share/application_%s.html' % self.object.application_type.lower()]


class ProjectList(SearchableListMixin, SortableListMixin, ListView):  # pylint: disable=too-many-ancestors
    '''Project List View'''
    sort_fields_aliases = [('name', 'by_name'), ('id', 'by_id'), ('votes', 'by_likes'), ]
    search_fields = [('application__name', 'iexact')]
    search_split = False
    model = Project
    paginate_by = 20
    ordering = ["-when"]

    def get_queryset(self):
        '''Return queryset'''
        set_of_approved_projects = Project.approved_projects()
        filter_val = self.request.GET.get('filter')
        if filter_val is not None:
            set_of_approved_projects = set_of_approved_projects.filter(application=filter_val,)
        order = self.request.GET.get('orderby')
        if order is not None:
            set_of_approved_projects = set_of_approved_projects.order_by(order)
        return set_of_approved_projects

    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        context['application_list'] = Application.objects.all()
        return super(ProjectList, self).render_to_response(context, **response_kwargs)


class ProjectTagList(ProjectList):  # pylint: disable=too-many-ancestors
    '''Project Tag List'''
    def get_queryset(self):
        '''Return Queryset'''
        self.tag = get_object_or_404(Tag, pk=self.kwargs['tag_pk'])
        return Project.approved_projects().filter(tags__in=[self.tag])


class ProjectDetail(RestrictPermissionMixin, DetailView):  # pylint: disable=too-many-ancestors
    '''Project Detail View'''
    queryset = \
        Project.objects.select_related("approval").select_related("owner").select_related("screenshot")

    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        object_to_render = self.get_object()
        context['hasApproval'] = \
            (hasattr(object_to_render, 'approval') or object_to_render.approved)
        return super(ProjectDetail, self).render_to_response(context, **response_kwargs)


class ProjectRunDetail(RestrictPermissionMixin, DetailView):  \
        # pylint: disable=too-many-ancestors
    '''Project Run Detail View'''
    model = Project
    template_name = "project_share/application_csnap.html"
    context_object_name = 'project'

    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        context['application'] = context['project'].application
        try:
            context['GOOGLE_ANALYTICS_PROPERTY_ID'] \
                = settings.GOOGLE_ANALYTICS_PROPERTY_ID
        except:
            pass
        return super(ProjectRunDetail, self).\
            render_to_response(context, **response_kwargs)


class ProjectPresentDetail(ProjectRunDetail): \
        # pylint: disable=too-many-ancestors
    '''Project Present Detail'''
    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        context['present'] = True
        return super(ProjectPresentDetail,
                     self).render_to_response(context, **response_kwargs)


class ProjectCreate(CreateView):  # pylint: disable=too-many-ancestors
    '''Project Create View'''
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        '''Get Success Url'''
        return reverse('project-update', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        self.kwargs = kwargs
        self.request = request
        return super(ProjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''Form Valid'''
        form.instance.owner = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):  # pylint: disable=too-many-ancestors
    '''Project Update'''
    model = Project
    form_class = ProjectForm

    template_name = "project_share/project_edit.html"

    def post(self, request, *args, **kwargs):
        '''Post'''
        if 'publish_project' in request.POST:
            super(ProjectUpdate, self).post(request, *args, **kwargs)
            project = super(ProjectUpdate, self).get_object()
            project.save()
            return redirect('approval-create', project_pk=project.pk)
        return super(ProjectUpdate, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        '''Get Form Kwargs'''
        kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        self.kwargs = kwargs
        self.request = request
        return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        '''Get Object'''
        gotten_object = super(ProjectUpdate, self).get_object()

        # If the object doesn't belong to this user, throw a error 503
        if gotten_object.owner != self.request.user \
                or (hasattr(gotten_object,
                            'approval') or gotten_object.approved):
            raise PermissionDenied()
        return gotten_object


class ProjectDelete(DeleteView):  # pylint: disable=too-many-ancestors
    '''Project Delete View'''
    model = Project
    success_url = reverse_lazy('project-delete-success')

    def get_object(self, queryset=None):
        '''Get Object'''
        gotten_object = super(ProjectDelete, self).get_object()
        if not gotten_object.owner == self.request.user:
            raise PermissionDenied('this isn\'t your project')
        return gotten_object


class ProjectUnpublish(UpdateView):  # pylint: disable=too-many-ancestors
    '''Project Unpublish'''
    model = Project
    template_name = "project_share/project_unpublish.html"
    form_class = ProjectUnpublishForm

    def post(self, request, *args, **kwargs):
        '''Post'''
        if 'Unpublish' in request.POST:
            proj = super(ProjectUnpublish, self).get_object()
            proj.approved = False
            proj.save()

            try:
                approval = Approval.objects.get(project_id=proj.id)
                approval.delete()
            except:
                pass

            try:
                ownership = Ownership.objects\
                    .filter(content_type_id=ContentType.objects.get_for_model(proj))\
                    .get(object_id=proj.id)
                ownership.delete()
            except:
                pass
            return redirect(reverse_lazy('project-unpublish-success'))
        return super(ProjectUnpublish, self).post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        self.kwargs = kwargs
        self.request = request
        return super(ProjectUnpublish, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        '''Get Object'''
        gotten_object = super(ProjectUnpublish, self).get_object()

        # If the object doesn't belong to this user, throw a error 503
        if gotten_object.owner != self.request.user:
            raise PermissionDenied('this isn\'t your project')
        return gotten_object


class DemoList(ListView):  # pylint: disable=too-many-ancestors
    '''Demo List View'''
    model = ApplicationDemo


class DemoDetail(DetailView):  # pylint: disable=too-many-ancestors
    '''Demo Detail View'''
    model = ApplicationDemo
    context_object_name = 'applicationdemo'
    template_name = "project_share/application_csnap.html"

    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        try:
            context['GOOGLE_ANALYTICS_PROPERTY_ID'] = \
                settings.GOOGLE_ANALYTICS_PROPERTY_ID
        except:
            pass
        return super(DemoDetail, self)\
            .render_to_response(context, **response_kwargs)


class ApprovalCreate(CreateView):  # pylint: disable=too-many-ancestors
    '''Approval Create View'''
    model = Approval
    form_class = ApprovalForm

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        self.kwargs = kwargs
        self.request = request
        return super(ApprovalCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''Post'''
        project_id = self.kwargs['project_pk']
        team_approval = Ownership()  # Create an ownership object
        team_approval.content_type = \
            ContentType.objects.get(app_label="project_share", model="project")
        team_approval.object_id = project_id
        if Project.objects.get(pk=project_id).classroom is None:
            team_approval = None
            return super(ApprovalCreate, self).post(request, *args, **kwargs)
        team_approval.team = Project.objects.get(pk=project_id).classroom
        team_approval.approved = False
        team_approval.save()
        return super(ApprovalCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        '''Form Valid'''
        form.instance.project_id = self.kwargs['project_pk']
        return super(ApprovalCreate, self).form_valid(form)

    def get_success_url(self):
        '''Get Success url'''
        return reverse('approval-confirm')


class UserDetail(DetailView):  # pylint: disable=too-many-ancestors
    '''User Detail View'''
    model = USER
    template_name = "project_share/user_detail.html"

    def render_to_response(self, context, **response_kwargs):
        '''Render to Response'''
        context['user'] = self.request.user
        return super(UserDetail, self)\
            .render_to_response(context, **response_kwargs)


class AddressCreate(CreateView):  # pylint: disable=too-many-ancestors
    '''Address Create View'''
    model = Address
    form_class = AddressForm

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        return u'/'


class AddressUpdate(UpdateView):  # pylint: disable=too-many-ancestors
    '''Address Update View'''
    model = Address
    form_class = AddressForm

    template_name = "project_share/address_form.html"

    def dispatch(self, request, *args, **kwargs):
        '''Dispatch'''
        if not request.user.id == int(self.kwargs['pk']):
            raise PermissionDenied
        return super(AddressUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''Get Success Url'''
        return reverse('address-confirm')
