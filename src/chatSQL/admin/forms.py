from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
class StrutturaDatabaseForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    
class TabellaForm(forms.Form):
    nome = forms.CharField(max_length=255, required=True, label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    sinonimi = forms.CharField(max_length=255, required=False, label="Sinonimi")
    struttura = forms.CharField(max_length=255, required=True, label="Struttura DB")    
    
class EliminaForm(forms.Form):
    classe_modello = forms.CharField(widget=forms.HiddenInput)
    id_modello = forms.IntegerField(widget=forms.HiddenInput)