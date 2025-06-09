from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='', label='Username')
    email = forms.EmailField(help_text='', label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': 'Enter a username for you',
            'password1': '',
            'password2': '',
        }
        

class LoginForm(AuthenticationForm):
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    

