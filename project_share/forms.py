from django import forms
from django.forms import ModelForm

from project_share.models import Project, Approval, Address, Classroom

class ProjectForm(ModelForm):
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super (ProjectForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['classroom'].queryset = Classroom.objects.filter(students=user)
        
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
