from django import forms

from .models import Interview

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['mp3_file', 'pic', 'full_name', 'slug', 'date', 'location', 'interview_by', 'birthplace', 'occupation', 'birth_year', 'summary', ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
        }

    def __init__(self, *args, **kwargs):
        slug = kwargs.pop('slug','')
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields['project']=forms.ModelChoiceField(queryset=OralHistory.objects.get(slug=slug))
