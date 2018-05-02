from django import forms

from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['mp3_file', 'pic', 'full_name', 'date',
                  'location', 'interview_by', 'birthplace', 'occupation',
                  'birth_year', 'summary', 'project', 'user']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        # slug = kwargs.pop('slug',None)
        super(InterviewForm, self).__init__(*args, **kwargs)
        # print('*****', slug)
        # oral_histories = get_object_or_404(OralHistory, slug=slug)
        # self.fields['project']=forms.ModelChoiceField(queryset=oral_histories)
