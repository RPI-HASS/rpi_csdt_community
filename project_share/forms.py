"""All the forms for creating and controlling projects, applications, and user."""
from django import forms
from django.forms import ModelForm
from django_teams.models import Team, TeamStatus

from project_share.models import (Address, Application, ApplicationCategory,
                                  Approval, Project)


class ProjectForm(ModelForm):
    """Form for project updating / creation."""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)  # populates the post
        # make sure we're only getting the right classrooms
        self.fields['classroom'].queryset = Team.objects.filter(users=user)

    class Meta:
        model = Project
        exclude = ('owner', 'approved', 'application', 'project', 'screenshot', 'parent')


class ProjectUnpublishForm(ModelForm):
    """Unpublishing form (not used)."""

    class Meta:
        model = Project
        exclude = ('owner', 'approved', 'application', 'project', 'screenshot', 'parent')


class ApprovalForm(ModelForm):
    """Used by teachers to approve projects."""

    class Meta:
        model = Approval
        exclude = ('project', 'when_requested', 'when_updated', 'approved_by')


class ExtendedSignupForm(forms.Form):
    """Signup form with many special placeholders for race gender etc."""

    gender = forms.CharField(max_length=100, label='gender',
                             widget=forms.TextInput(attrs={'placeholder': 'gender (optional)'}), required=False)
    race = forms.CharField(max_length=100, label='race',
                           widget=forms.TextInput(attrs={'placeholder': 'race (optional)'}), required=False)
    age = forms.IntegerField(label='age', widget=forms.TextInput(attrs={'placeholder': 'age (optional)'}),
                             required=False)
    classroom = forms.IntegerField(label='classroom',
                                   widget=forms.TextInput(attrs={'placeholder': 'classroom # (optional)'}),
                                   required=False)
    field_order = ['username', 'email', 'password1', 'password2', 'gender', 'race', 'age', 'classroom']

    def signup(self, request, n_user):
        """specify where to put race / gender data, and signup for classroom"""
        n_user.gender = self.cleaned_data['gender']
        n_user.race = self.cleaned_data['race']
        n_user.age = self.cleaned_data['age']
        n_user.save()
        team = self.cleaned_data['classroom']
        if team is not None:
            TeamStatus(team=Team.objects.get(pk=team), role=1, user=n_user, comment='just signed up').save()


class AddressForm(ModelForm):
    """Not used."""

    class Meta:
        model = Address
        exclude = ('teacher',)


class ApplicationAdminForm(ModelForm):
    """Helpful hints for selection of categories for application."""

    categories = forms.ModelMultipleChoiceField(label='Categories',
                                                queryset=ApplicationCategory.objects.all(), required=False,
                                                help_text='Select which categories this application belongs too; \
                                                think about multiple themes (computing, \
                                                math, cultural)')

    class Meta:
        model = Application
        exclude = ()
