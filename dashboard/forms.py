from django import forms

# Import user authentication forms
from django.contrib.auth.forms import UserCreationForm

# Import Auth Models
from django.contrib.auth.models import User

# Import models
from .models import (Profile, Contractor)

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    contactor = forms.ModelChoiceField(queryset=Contractor.objects.filter(is_active=True))