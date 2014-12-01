from django import forms
from django.forms import ModelForm

from project_share.models import Project, Approval, Address

class ProjectForm(ModelForm):
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
