from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")