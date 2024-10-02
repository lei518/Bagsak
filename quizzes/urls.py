from django.urls import path
from .views import *

app_name = 'quizzes'

urlpatterns = [
    # Viewing or interacting with a specific quiz (expects integer course_pk and quiz_pk)
    path('course/<int:course_pk>/<int:quiz_pk>/', quiz_view, name='quiz_view'),

    # Saving the quiz results (course_pk and quiz_pk as integers)
    path('course/<int:course_pk>/<int:quiz_pk>/save', save_quiz_view, name='save_view'),

    # Fetching quiz data (again course_pk and quiz_pk as integers)
    path('course/<int:course_pk>/<int:quiz_pk>/data', quiz_data_view, name='quiz_data_view'),

    # Step 1 URL
    path('course/<int:course_id>/create_quiz/', create_quiz, name='create_quiz'),

    # Step 2 URL (Important for this issue)
    path('course/<int:course_id>/create_quiz/step2/', create_quiz_step2, name='create_quiz_step2'),
]

