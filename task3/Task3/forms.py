from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile

# registration form 
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='', label='Username')
    email = forms.EmailField(help_text='', label='Email')


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Which fields to include


# Login Form
class LoginForm(AuthenticationForm):
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    

# Profile Details Displaying and editing form
class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows':4, 'cols':40}),
            'profile_picture': forms.TextInput(attrs={'placeholder': 'URL of your profile picture'}),
        }
