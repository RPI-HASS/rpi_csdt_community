from django import forms
from django.core import validators

from .models import Interview, OralHistory, Tag
from django_teams.models import Team


class InterviewForm(forms.ModelForm):
    classroom = forms.ChoiceField()

    class Meta:
        model = Interview
        fields = ['mp3_file', 'pic', 'full_name', 'date',
                  'location', 'interview_by', 'birthplace', 'occupation',
                  'birth_year', 'summary', 'project', 'user', ]
        exclude = ['csdt_project']

        widgets = {
            'summary': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def save(self, commit=True):
        # do something with self.cleaned_data['temp_id']

        return super(InterviewForm, self).save(commit=commit)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields['classroom'].choices = [
            (choice.pk, choice) for choice in Team.objects.filter(users=self.user)]


class OHPForm(forms.ModelForm):
    class Meta:
        model = OralHistory
        exclude = ['is_official', 'approved']

        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OHPForm, self).__init__(*args, **kwargs)


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class TagForm(forms.ModelForm):
    hours = forms.IntegerField(label='Hour')
    mins = forms.IntegerField(label='Minute')
    secs = forms.IntegerField(label='Second')
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput,
                               label="Leave empty", validators=[must_be_empty])

    class Meta:
        model = Tag
        exclude = ['interview', 'timestamp', 'approved']
