from django.contrib import admin
from django_pre_post.models import Answer, Question, Questionnaire, Attempt, QuestionOrder
from django_pre_post.util import AnswerDisplay, ExpectedAnswerDisplay


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "questionnaire", "attempt", "owner", 'relevant_answer', 'created', 'modified']
    list_display_links = ["question"]
    fields = ('question', 'owner', 'attempt', 'textAnswer', 'numericAnswer', 'multipleChoiceAnswer')
    readonyfields = ('created', 'modified')

    def relevant_answer(self, obj):
        return AnswerDisplay(self, obj)

    def questionnaire(self, obj):
        return obj.attempt.questionnaire


class QuestionOrderInline(admin.TabularInline):
    model = QuestionOrder
    extra = 1


class AnswerReadonlyInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'relevant_answer')
    fields = ('question', 'relevant_answer',)

    def relevant_answer(self, obj):
        return AnswerDisplay(self, obj)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'content', 'expected_answer', 'created', 'modified']
    list_filter = ["questionnaire", "type"]
    search_fields = ["content"]

    def question_type(self, obj):
        return obj.get_type_display()

    def expected_answer(self, obj):
        return ExpectedAnswerDisplay(self, obj)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'team', 'created', 'modified', 'public']
    list_filter = ["owner", "team"]
    search_fields = ["name", "owner", 'team']
    inlines = (QuestionOrderInline,)


class AttemptAdmin(admin.ModelAdmin):
    list_display = ['questionnaire', 'owner', 'created', 'modified']
    list_filter = ['questionnaire', 'owner']
    search_fields = ['questionnaire', 'owner']
    fields = (('questionnaire', 'owner'),)
    inlines = (AnswerReadonlyInline,)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Attempt, AttemptAdmin)
