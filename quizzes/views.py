from django.shortcuts import render,redirect, get_object_or_404
from class_app.models import Course
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import QuizForm, QuestionFormSet, AnswerFormSet
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from .forms import QuizForm, QuestionForm, AnswerForm, QuizSetupForm

class QuizListView(ListView):
    model = Quiz
    template_name = 'course.html'


def quiz_view(request, course_pk, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    return render(request, 'quiz.html', {'quiz': quiz})


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


def save_quiz_view(request, course_pk, quiz_pk):
    # Ensure the request is a POST request and is sent via AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Extract the POST data
            data = request.POST
            print(f"Received data: {data}")

            # Validate the presence of the CSRF token
            if 'csrfmiddlewaretoken' not in data:
                return JsonResponse({'error': 'CSRF token missing'}, status=400)

            # Initialize dictionary for quiz answers
            quiz_answers = {}

            # Iterate over POST data and skip 'csrfmiddlewaretoken'
            for key, value in data.items():
                if key != 'csrfmiddlewaretoken':  # Skip CSRF token
                    quiz_answers[key] = value  # Save the answer for each question

            print(f"Parsed answers: {quiz_answers}")

            # Fetch the quiz and its related questions
            quiz = Quiz.objects.get(pk=quiz_pk)
            user = request.user
            questions = quiz.question_set.all()  # Get all questions in the quiz

            # Initialize score and results list
            score = 0
            total_questions = questions.count()
            results = []

            # Iterate through all questions in the quiz
            for question in questions:
                # Get the user's answer for the current question
                selected_answer = quiz_answers.get(question.text)

                # Fetch the correct answer from the database
                correct_answer = question.get_correct_answer()

                # If no answer is selected, treat it as wrong
                if not selected_answer:
                    results.append({
                        str(question): {
                            'correct': False,
                            'selected_answer': 'None',
                            'correct_answer': correct_answer.text if correct_answer else 'None'
                        }
                    })
                elif selected_answer == correct_answer.text:
                    # If the selected answer matches the correct answer
                    score += 1
                    results.append({
                        str(question): {
                            'correct': True,
                            'selected_answer': selected_answer,
                            'correct_answer': correct_answer.text
                        }
                    })
                else:
                    # If the selected answer is incorrect
                    results.append({
                        str(question): {
                            'correct': False,
                            'selected_answer': selected_answer,
                            'correct_answer': correct_answer.text
                        }
                    })

            # Calculate the final score as a percentage
            final_score = (score / total_questions) * 100
            print(f"Final score: {final_score}% score: {score}")

            # Check if the user passed or failed based on the required score to pass
            passed = final_score >= quiz.req_score_to_pass

            # Send the score, results, and passing status to the frontend
            return JsonResponse({
                'success': True,
                'message': 'Quiz saved successfully!',
                'score': final_score,
                'results': results,
                'passed': passed,
                'passing_score': quiz.req_score_to_pass  # Send the passing score to the frontend
            })

        except Exception as e:
            # Log and return any error encountered
            print(f"Error processing quiz submission: {e}")
            return JsonResponse({'error': 'An error occurred while processing your submission.'}, status=500)

    # If the request isn't a valid AJAX POST, return an error
    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
@user_passes_test(lambda u: u.is_professor)
def create_quiz(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Step 1: Get the number of questions and choices
    if request.method == 'POST' and 'setup_quiz' in request.POST:
        setup_form = QuizSetupForm(request.POST)
        if setup_form.is_valid():
            num_questions = setup_form.cleaned_data['number_of_questions']
            choices_per_question = setup_form.cleaned_data['choices_per_question']

            # Store these values in the session to access them in the next step
            request.session['num_questions'] = num_questions
            request.session['choices_per_question'] = choices_per_question

            return redirect('create_quiz_step2', course_id=course_id)

    else:
        setup_form = QuizSetupForm()

    return render(request, 'setup_quiz.html', {'setup_form': setup_form, 'course': course})

# Step 2: Display dynamic formsets based on input from Step 1
@login_required
@user_passes_test(lambda u: u.is_professor)
def create_quiz_step2(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Get the number of questions and choices from the session
    num_questions = request.session.get('num_questions', None)
    choices_per_question = request.session.get('choices_per_question', None)

    if not num_questions or not choices_per_question:
        return redirect('create_quiz', course_id=course_id)

    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=num_questions)
    AnswerFormSet = modelformset_factory(Answer, form=AnswerForm, extra=choices_per_question)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.course = course
            quiz.save()

            questions = question_formset.save(commit=False)
            for index, question in enumerate(questions):
                question.quiz = quiz
                question.save()

                # Save answers for each question
                answer_formset = AnswerFormSet(request.POST, prefix=f'answers-{index}')
                if answer_formset.is_valid():
                    answers = answer_formset.save(commit=False)
                    for answer in answers:
                        answer.question = question
                        answer.save()

            return redirect('course_view', pk=course.pk)
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none(), prefix='questions')
        answer_formsets = [
            AnswerFormSet(queryset=Answer.objects.none(), prefix=f'answers-{i}')
            for i in range(num_questions)
        ]

    context = {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'answer_formsets': answer_formsets,
        'course': course,
    }
    return render(request, 'create_quiz.html', context)
