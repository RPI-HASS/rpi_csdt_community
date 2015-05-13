from django import forms
from django.forms import ModelForm

from project_share.models import Project, Approval, Address, Application, ApplicationCategory
from django_teams.models import Team

class ProjectForm(ModelForm):
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super (ProjectForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['classroom'].queryset = Team.objects.filter(users=user) # make sure we're only getting the right classrooms

    class Meta:
        model = Project
        exclude = ('owner', 'approved','application','project','screenshot','parent',)

class ApprovalForm(ModelForm):
    class Meta:
        model = Approval
        exclude = ('project', 'when_requested', 'when_updated', 'approved_by',)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('teacher',)

class ApplicationAdminForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(label='Categories',
        queryset=ApplicationCategory.objects.all(), required=False,
        help_text='Select which categories this application belongs too; think about multiple themes (computing, math, cultural)')


    class Meta:
        model = Application
