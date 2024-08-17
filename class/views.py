from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from .models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_student:
            auth_login(request, user)
            return redirect('home_view')  # Redirect to the home view after successful login
        elif user is not None and user.is_professor:
            auth_login(request, user)
            return redirect('professor_dashboard')
        else:
            messages.error(request, "Invalid username or password.")  # Add an error message
            return render(request, 'login.html')  # Render the login page again with an error
    else:
        return render(request, 'login.html')


def professor_dashboard(request):
    # Code to render the professor dashboard
    return render(request, 'prof.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Redirect to a success page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
