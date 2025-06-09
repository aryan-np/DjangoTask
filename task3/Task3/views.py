from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm,ProfileDetailsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login as auth_login
from .models import Profile


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
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = ProfileDetailsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileDetailsForm(instance=profile)
        
    return render(request, 'task3/profile.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')