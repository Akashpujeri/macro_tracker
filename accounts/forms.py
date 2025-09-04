from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'weight', 'height', 'activity_level', 'goal']

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }