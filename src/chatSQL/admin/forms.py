from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
   username = forms.CharField(label="Nome Utente")
   password = forms.CharField(widget=forms.PasswordInput(), label="Password")