"""All the forms for creating and controlling projects, applications, and user."""
from django import forms
from django.forms import ModelForm
from django_teams.models import Team, TeamStatus
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from snowpenguin.django.recaptcha2.widgets import ReCaptchaHiddenInput
from project_share.models import (Application, ApplicationCategory,
                                  Approval, Project)

from .models import ExtendedUser


class ProjectForm(ModelForm):
    """Form for project updating / creation."""

    def __init__(self, *args, **kwargs):
        classrooms = None
        if 'user' in kwargs:
            user = kwargs.pop('user')
            classrooms = Team.objects.filter(users=user)
            if kwargs['instance'].classroom is None:
                kwargs.update(initial={
                    # 'field': 'value'
                    'classroom': classrooms.first()
                })
        super(ProjectForm, self).__init__(*args, **kwargs)  # populates the post
        # make sure we're only getting the right classrooms
        if classrooms is not None:
            self.fields['classroom'].queryset = classrooms

    class Meta:
        model = Project
        exclude = ('owner', 'approved', 'when_created', 'when_modified',
                   'application', 'project', 'screenshot', 'parent', 'mark', 'comment')


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

    username = forms.CharField(max_length=100, label='username',
                               widget=forms.TextInput(attrs={'placeholder': 'username (no spaces)'}), required=False)
    email = forms.CharField(max_length=100, label='email',
                            widget=forms.TextInput(attrs={'placeholder': 'email address'}), required=False)
    # gender = forms.CharField(max_length=100, label='gender',
    #                          widget=forms.TextInput(attrs={'placeholder': 'gender (optional)'}), required=False)
    # race = forms.CharField(max_length=100, label='race',
    #                        widget=forms.TextInput(attrs={'placeholder': 'race (optional)'}), required=False)
    # age = forms.IntegerField(label='age', widget=forms.TextInput(attrs={'placeholder': 'age (optional)'}),
    #                          required=False)
    classroom = forms.IntegerField(label='classroom',
                                   widget=forms.TextInput(attrs={'placeholder': 'classroom # (optional)'}),
                                   required=False)
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())

    field_order = ['username', 'email', 'password1', 'password2', 'classroom', 'captcha']

    def signup(self, request, n_user):
        """specify where to put race / gender data, and signup for classroom"""
        # n_user.gender = self.cleaned_data['gender']
        # n_user.race = self.cleaned_data['race']
        # n_user.age = self.cleaned_data['age']
        n_user.save()
        team = self.cleaned_data['classroom']
        if team is not None:
            TeamStatus(team=Team.objects.get(pk=team), role=1, user=n_user, comment='just signed up').save()


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ['email', 'username', 'display_name', 'avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }
