from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or your desired page
    else:
        form = RegisterForm()
    return render(request, 'task3/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')  # Redirect to profile or home page
    else:
        form = LoginForm()
    return render(request, 'task3/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'task3/profile.html')