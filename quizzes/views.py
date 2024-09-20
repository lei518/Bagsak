from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse

class QuizListView(ListView):
    model = Quiz
    template_name = 'course.html'


def quiz_view(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)  # Use quiz_pk here
    return render(request, 'quiz.html', {'quiz_info': quiz})


from django.http import JsonResponse
from .models import Quiz


def quiz_data_view(request, course_pk, quiz_pk):
    try:
        # Fetch the quiz and its questions
        quiz = Quiz.objects.get(pk=quiz_pk)
        questions = []
        for q in quiz.get_questions():
            answers = [a.text for a in q.get_answers()]
            questions.append({str(q): answers})

        # Return JSON response
        return JsonResponse({
            'data': questions,
            'time': quiz.time,
        })

    # Handle the case where the quiz doesn't exist
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    # Catch other exceptions
    except Exception as e:
        print(f"Error: {e}")  # Print error to server logs for debugging
        return JsonResponse({'error': 'An error occurred'}, status=500)

