from django.urls import path
from .views import quiz_view,QuizListView,quiz_data_view


app_name = 'quizzes'

urlpatterns = [

path('course/<course_pk>/<quiz_pk>/', quiz_view, name='quiz_view'),
path('course/<course_pk>/<quiz_pk>/data', quiz_data_view, name='quiz_data_view'),
]
