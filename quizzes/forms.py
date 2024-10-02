from django import forms
from django.forms import inlineformset_factory
from .models import Quiz
from questions.models import Question, Answer

# Quiz form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'course', 'topic', 'time', 'req_score_to_pass']  # 'no_of_questions' removed

# Question form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

# Answer form with the 'correct' field to mark correct answers
class AnswerForm(forms.ModelForm):
    correct = forms.BooleanField(required=False, label="Mark as correct")  # Explicit correct answer checkbox

    class Meta:
        model = Answer
        fields = ['text', 'correct']

# Formset for questions (inline formset between Quiz and Question)
QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    extra=1,  # This can be dynamically adjusted based on user input in the view
    can_delete=True
)

# Formset for answers (inline formset within questions)
AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=2,  # Default to two answers per question, dynamically adjustable
    can_delete=True
)

# Quiz setup form for specifying the number of questions and choices per question
class QuizSetupForm(forms.Form):
    number_of_questions = forms.IntegerField(min_value=1, label="Number of Questions")
    choices_per_question = forms.IntegerField(min_value=2, label="Choices per Question")
