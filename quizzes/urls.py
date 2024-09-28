from django.urls import path
from .views import quiz_view, QuizListView, quiz_data_view, save_quiz_view, create_quiz, create_quiz_step2

app_name = 'quizzes'

urlpatterns = [
    # Viewing or interacting with a specific quiz (expects integer course_pk and quiz_pk)
    path('course/<int:course_pk>/<int:quiz_pk>/', quiz_view, name='quiz_view'),

    # Saving the quiz results (course_pk and quiz_pk as integers)
    path('course/<int:course_pk>/<int:quiz_pk>/save', save_quiz_view, name='save_view'),

    # Fetching quiz data (again course_pk and quiz_pk as integers)
    path('course/<int:course_pk>/<int:quiz_pk>/data', quiz_data_view, name='quiz_data_view'),

    # Step 1: Creating a new quiz, only course_id is needed (as an integer)
    path('course/<int:course_id>/create_quiz/', create_quiz, name='create_quiz'),

    # Step 2: Dynamic question and answer input based on number of questions and choices
    path('course/<int:course_id>/create_quiz/create_quiz_step2/', create_quiz_step2, name='create_quiz_step2'),
]
