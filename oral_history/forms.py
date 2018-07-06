from django import forms

from .models import Interview, OralHistory, Tag
from django_teams.models import Team


class InterviewForm(forms.ModelForm):
    mp3_file = forms.FileField(required=False, label="Mp3 file that's <50mb \
        (tip: make mono and <=96kbps bitrate)")
    classroom = forms.ChoiceField(required=False)
    date = forms.DateField(label='Date of interview in format YYYY-MM-DD')
    location = forms.CharField(label='Location of Interview', max_length=70)

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
        self.fields['classroom'].choices = []
        self.fields['classroom'].choices.append(('', '---------------'))
        test = [(choice.pk, choice) for choice in Team.objects.filter(users=self.user)]
        self.fields['classroom'].choices += test
        


class OHPForm(forms.ModelForm):
    class Meta:
        model = OralHistory
        exclude = ['is_official', 'approved', 'slug']

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
