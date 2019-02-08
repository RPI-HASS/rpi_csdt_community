from django.core.exceptions import PermissionDenied
from django_pre_post.forms import CSRFQuestionnaireForm
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django_pre_post.models import Questionnaire, Question, Answer, Attempt
from django_pre_post.util import TemplateBoolean
from django.core.urlresolvers import reverse


class FillOutQuestionnaire(UpdateView):
    model = Questionnaire
    fields = ['name', 'questions']

    def get_success_url(self):
        print('test2')
        return reverse('successful-submission')

    def get_object(self):
        obj = super(FillOutQuestionnaire, self).get_object()
        if (not obj.public and obj.owner != self.request.user) and not self.request.user.is_superuser:
            raise PermissionDenied()
        self.object = obj
        return obj

    def post(self, request, *args, **kwargs):
        form = CSRFQuestionnaireForm(request.POST)
        if form.is_valid():
            attempt = Attempt(questionnaire=self.get_object(), owner=request.user)
            attempt.save()
            for item in request.POST:
                try:
                    question = Question.objects.get(id=item)
                    if question.get_type_display() == 'Multiple Choice':
                        answer = Answer(question=question, owner=request.user,
                                        attempt=attempt, multipleChoiceAnswer=request.POST[item])
                    elif question.get_type_display() == 'Numeric' or question.get_type_display() == 'Rank':
                        answer = Answer(question=question, owner=request.user,
                                        attempt=attempt, numericAnswer=request.POST[item])
                    else:
                        answer = Answer(question=question, owner=request.user,
                                        attempt=attempt, textAnswer=request.POST[item])
                    answer.save()
                except:  # noqa: E722
                    pass
        return HttpResponseRedirect(self.get_success_url())

    def render_to_response(self, context, **response_kwargs):
        context['doingRankings'] = TemplateBoolean()
        context['questions'] = self.get_object().questions.order_by('questionorder')
        return super(FillOutQuestionnaire, self).render_to_response(context, **response_kwargs)


class FramelessQuestionnaire(FillOutQuestionnaire):
    template_name = "django_pre_post/frameless_questionnaire.html"
