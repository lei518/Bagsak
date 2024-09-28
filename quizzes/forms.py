from django import forms
from django.forms import inlineformset_factory
from .models import Quiz
from questions.models import Question, Answer
from django import forms

# Quiz form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'course', 'topic', 'no_of_questions', 'time', 'req_score_to_pass']

# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

# Answer form
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']

# Formset for questions (inline formset)
QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    extra=1,  # You can adjust the number of extra forms
    can_delete=True
)

# Formset for answers (inline formset within questions)
AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=2,  # Default two answers per question
    can_delete=True
)


class QuizSetupForm(forms.Form):
    number_of_questions = forms.IntegerField(min_value=1, label="Number of Questions")
    choices_per_question = forms.IntegerField(min_value=2, label="Choices per Question")
