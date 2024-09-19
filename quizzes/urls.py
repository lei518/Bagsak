from django.urls import path
from .views import quiz_view,QuizListView


app_name = 'quizzes'

urlpatterns = [

path('course/<course_pk>/<quiz_pk>/', quiz_view, name='quiz_view'),

]
