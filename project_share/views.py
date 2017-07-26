"""Defines the displays for projects, applications, demos, and goals."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_teams.models import Ownership
from extra_views import SearchableListMixin, SortableListMixin
from taggit.models import Tag

from project_share.forms import (AddressForm, ApprovalForm, ProjectForm,
                                 ProjectUnpublishForm)
from project_share.models import (Address, Application, ApplicationDemo,
                                  Approval, Project)

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from . import forms


def filter_project_query(set, request):
    filter_val = request.GET.get('filter')
    if filter_val is not None:
        set = set.filter(application=filter_val,)
    term = request.GET.get('q')
    if term is not None:
        set = set.filter(Q(name__icontains=term) | Q(
            description__icontains=term) | Q(
            owner__username__icontains=term))
    order = request.GET.get('orderby')
    if order is not None:
        set = set.order_by(order)
    else:
        set = set.order_by("-id")
    return set


class RestrictPermissionMixin(object):
    """Prevent inappropriate access."""

    def dispatch(self, request, *args, **kwargs):
        """Same keywords and request."""
        self.kwargs = kwargs
        self.request = request
        return super(RestrictPermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """Return object is right owner or public, else permision denied."""
        if hasattr(self, 'object'):
            return self.object
        obj = super(RestrictPermissionMixin, self).get_object()

        # If the object doesn't belong to this user and isn't published, throw a error 403
        if (not obj.approved and obj.owner != self.request.user) and not self.request.user.is_superuser:
            raise PermissionDenied()
        self.object = obj
        return obj


class ApplicationList(ListView):
    """Stub displays all applications based on serializer."""

    model = Application


class ApplicationDetail(DetailView):
    """Stub displays all application info based on serializer."""

    model = Application


class ApplicationRunDetail(DetailView):
    """Run application (CSnap) as template and add in the analytics key."""

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


class ProjectList(SearchableListMixin, SortableListMixin, ListView):
    """List all projects, but make sortable."""

    sort_fields_aliases = [('name', 'by_name'), ('id', 'by_id'), ('votes', 'by_likes'), ]
    search_fields = [('application__name', 'iexact')]
    search_split = False
    model = Project
    paginate_by = 20
    ordering = ["-when"]

    def get_queryset(self):
        """Order projects based on filter or order request settings."""
        queryset = Project.approved_projects()
        return filter_project_query(queryset, self.request)

    def render_to_response(self, context, **response_kwargs):
        """List all applications for the user to choose to filter by."""
        application_list = Application.objects.all()
        context['application_list'] = application_list
        context['order'] = self.request.GET.get('orderby')
        filter_val = self.request.GET.get('filter')
        context['filter_val'] = filter_val
        if filter_val:
            context['name'] = application_list.get(id=filter_val)
        context['term'] = self.request.GET.get('q')
        return super(ProjectList, self).render_to_response(context, **response_kwargs)


class ProjectTagList(ProjectList):
    """List all the tags of various projects. Not used."""

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['tag_pk'])
        return Project.approved_projects().filter(tags__in=[self.tag])


class ProjectDetail(DetailView):
    """Display all the information about a project given owner is correct."""

    queryset = Project.objects.select_related("approval").select_related("owner").select_related("screenshot")

    def render_to_response(self, context, **response_kwargs):
        """Check owner or approval."""
        obj = self.get_object()
        context['hasApproval'] = (hasattr(obj, 'approval') or obj.approved)
        return super(ProjectDetail, self).render_to_response(context, **response_kwargs)


class ProjectRunDetail(DetailView):
    """Run the project as the same template as application but with application,
    but with settings for application and analytics."""

    model = Project
    template_name = "project_share/application_csnap.html"
    context_object_name = 'project'

    def render_to_response(self, context, **response_kwargs):
        context['application'] = context['project'].application
        try:
            context['GOOGLE_ANALYTICS_PROPERTY_ID'] = settings.GOOGLE_ANALYTICS_PROPERTY_ID
        except:
            pass
        return super(ProjectRunDetail, self).render_to_response(context, **response_kwargs)


class ProjectPresentDetail(ProjectRunDetail):
    """Set the project into present (full screen) mode."""

    def render_to_response(self, context, **response_kwargs):
        context['present'] = True
        return super(ProjectPresentDetail, self).render_to_response(context, **response_kwargs)


class ProjectCreate(CreateView):
    """Simple create view but sets owner and returns to project when done."""

    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        """Return to project when done."""
        return reverse('project-update', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        """Keep everything and create."""
        self.kwargs = kwargs
        self.request = request
        return super(ProjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Owner is project creator."""
        form.instance.owner = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(UpdateView):
    """Add and or change info on a project or submit for approval."""

    model = Project
    form_class = ProjectForm

    template_name = "project_share/project_edit.html"

    def post(self, request, *args, **kwargs):
        """Submit for approval."""
        obj = super(ProjectUpdate, self).get_object()
        if 'publish_project' in request.POST and not (hasattr(obj, 'approval')):
            super(ProjectUpdate, self).post(request, *args, **kwargs)
            obj.save()
            return redirect('approval-create', project_pk=obj.pk)
        return super(ProjectUpdate, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """define the user as the person submitting request."""
        kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        """Keep everything and run update."""
        self.kwargs = kwargs
        self.request = request
        return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """If the object doesn't belong to this user, throw a error 503."""
        obj = super(ProjectUpdate, self).get_object()
        if obj.owner != self.request.user or obj.approved:
            raise PermissionDenied()
        return obj


class ProjectDelete(DeleteView):
    """Delete projet."""

    model = Project
    success_url = reverse_lazy('project-delete-success')

    def get_object(self, queryset=None):
        """Only delete if owner."""
        obj = super(ProjectDelete, self).get_object()
        if not obj.owner == self.request.user:
            raise PermissionDenied('this isn\'t your project')
        return obj


class ProjectUnpublish(UpdateView):
    """Unpublish (not used)."""

    model = Project
    template_name = "project_share/project_unpublish.html"
    form_class = ProjectUnpublishForm

    def post(self, request, *args, **kwargs):
        """Change ownership, Delete approval request, change approval."""
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
                ownership = Ownership.objects.filter(content_type_id=ContentType.objects.get_for_model(proj)).get(
                    object_id=proj.id)
                ownership.delete()
            except:
                pass
            return redirect(reverse_lazy('project-unpublish-success'))
        return super(ProjectUnpublish, self).post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Keep everything and submit change."""
        self.kwargs = kwargs
        self.request = request
        return super(ProjectUnpublish, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """If the object doesn't belong to this user, throw a error 503."""
        obj = super(ProjectUnpublish, self).get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied('this isn\'t your project')
        return obj


class DemoList(ListView):
    """Stub uses serializer for demo list."""

    model = ApplicationDemo


class DemoDetail(DetailView):
    """Run the demo (should be called demorundetail) & set the analytics property."""

    model = ApplicationDemo
    context_object_name = 'applicationdemo'
    template_name = "project_share/application_csnap.html"

    def render_to_response(self, context, **response_kwargs):
        """Set the analytics property."""
        try:
            context['GOOGLE_ANALYTICS_PROPERTY_ID'] = settings.GOOGLE_ANALYTICS_PROPERTY_ID
        except:
            pass
        return super(DemoDetail, self).render_to_response(context, **response_kwargs)


class ApprovalCreate(CreateView):
    """Create an approval request for a project."""

    model = Approval
    form_class = ApprovalForm

    def dispatch(self, request, *args, **kwargs):
        """Keep everything and create approval."""
        self.kwargs = kwargs
        self.request = request
        return super(ApprovalCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create an ownership object."""
        project_id = self.kwargs['project_pk']
        team_approval = Ownership()
        team_approval.content_type = ContentType.objects.get(app_label="project_share", model="project")
        team_approval.object_id = project_id
        if Project.objects.get(pk=project_id).classroom is None:
            team_approval = None
            return super(ApprovalCreate, self).post(request, *args, **kwargs)
        team_approval.team = Project.objects.get(pk=project_id).classroom
        team_approval.approved = False
        team_approval.save()

        return super(ApprovalCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """make sure it's for the right project."""
        form.instance.project_id = self.kwargs['project_pk']
        return super(ApprovalCreate, self).form_valid(form)

    def get_success_url(self):
        """simple confirm page."""
        return reverse('approval-confirm')


class UserDetail(DetailView):
    """Show info for the user."""

    model = User
    template_name = "project_share/user_detail.html"

    def return_appl(self):
        filter_val = self.request.GET.get('filter')
        name = Application.objects.get(id=filter_val)
        return name

    def render_to_response(self, context, **response_kwargs):
        """Include define the projects, and allow search"""
        try:
            queryset = Project.objects.filter(
                Q(owner=self.object)).filter(Q(approved=True) | Q(owner=self.request.user)).order_by('-id')
        except:
            queryset = Project.objects.filter(Q(owner=self.object), Q(approved=True)).order_by('-id')

        context['project_list'] = filter_project_query(queryset, self.request)
        application_list = Application.objects.all()
        context['application_list'] = application_list
        context['order'] = self.request.GET.get('orderby')
        filter_val = self.request.GET.get('filter')
        context['filter_val'] = filter_val
        if filter_val:
            context['name'] = application_list.get(id=filter_val)
        context['term'] = self.request.GET.get('q')
        return super(UserDetail, self).render_to_response(context, **response_kwargs)


class AddressCreate(CreateView):
    """Not used."""

    model = Address
    form_class = AddressForm

    def form_valid(self, form):
        """set the teacher who is requesting the creation."""
        form.instance.teacher = self.request.user
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        """Go to the user page."""
        return u'/'


class AddressUpdate(UpdateView):
    """Not used."""

    model = Address
    form_class = AddressForm

    template_name = "project_share/address_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Only the user can change this."""
        if(not request.user.id == int(self.kwargs['pk'])):
            raise PermissionDenied
        return super(AddressUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Show confirmation."""
        return reverse('address-confirm')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


class ProfileUpdate(LoginRequiredMixin, DetailView, FormView):
    template_name = 'project_share/user_update.html'
    form_class = forms.ProfileForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('extendeduser-detail', kwargs={'pk': self.request.user.id}))

    def get_initial(self):
        return {'email': self.request.user.email,
                'username': self.request.user.username,
                'display_name': self.request.user.display_name,
                'avatar': self.request.user.avatar,
                'bio': self.request.user.bio,
                'age': self.request.user.age,
                'race': self.request.user.race,
                'gender': self.request.user.gender,
                }

    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # assign the object to the view
        form = MyUserChangeForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            if request.FILES:
                profile.avatar = request.FILES['avatar']
                file_type = profile.avatar.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    profile.avatar = None
                    messages.warning(request, "Avatar must be in jpg, jpeg, gif, or png format")
                    return render(request, "project_share/user_detail.html",
                                  {'object': self.request.user, 'form': form})
            profile.save()
            form.save()
            return self.form_valid(form)
        else:
            form = MyUserChangeForm(instance=request.user)
            return self.form_invalid(form)


class MyUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ('email', 'username', 'display_name', 'avatar', 'bio', 'gender', 'race', 'age')
