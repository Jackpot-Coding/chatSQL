from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
class DatabaseStructureForm(forms.Form):
    name = forms.CharField(label="Nome")
    description = forms.CharField(widget=forms.Textarea, label="Descrizione")