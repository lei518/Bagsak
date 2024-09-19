from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView

class QuizListView(ListView):
    model = Quiz
    template_name = 'course.html'


def quiz_view(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)  # Use quiz_pk here
    return render(request, 'quiz.html', {'quiz_info': quiz})

# Create your views here.
