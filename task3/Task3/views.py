from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm,ProfileDetailsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login as auth_login
from .models import Profile


# view for registration
def register(request):
    """
    Handle user registration.

    GET:
        - Render the registration form.

    POST:
        - Validate and save the new user data.
        - Redirect to the login page on successful registration.
    """
    # for post method
    if request.method == 'POST':
        # pass post request data to form
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to login page after successful registration
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'task3/register.html', {'form': form})


# view for login
def login(request):
    """
    Handle user login.

    GET:
        - Render the login form.

    POST:
        - Validate credentials and authenticate user.
        - Redirect to profile page on successful login.
    """
    # for post method
    if request.method == 'POST':
        # pass post request data to form
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')  # Redirect to profile 
    else:
        form = LoginForm()
    return render(request, 'task3/login.html', {'form': form})


@login_required #ensures only authenticated user can access
def profile(request):
    """
    Display and update user profile details.

    GET:
        - Render the profile form populated with existing data.

    POST:
        - Validate and save updates to the profile.
        - Redirect to the profile page after saving.
    """
    # retrive user from request
    user = request.user
    # get or create profile if not exist
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        #passing instance to edit in existing instead of creating new
        form = ProfileDetailsForm(request.POST, instance=profile) 
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileDetailsForm(instance=profile)
        
    return render(request, 'task3/profile.html', {'form': form})



def logout_view(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    return redirect('login')