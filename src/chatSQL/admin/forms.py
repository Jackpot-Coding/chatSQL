from django import forms
from .enums import TipoCampo

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
class StrutturaDatabaseForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    
class EliminaForm(forms.Form):
    classe_modello = forms.CharField(widget=forms.HiddenInput)
    id_modello = forms.IntegerField(widget=forms.HiddenInput)

class TabellaForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    sinonimi = forms.CharField(label="Sinonimi", required=False)

class CampoTabella(forms.Form):
    nome=forms.CharField(label="Nome")
    tipo=forms.ChoiceField(choices=[(tag.value, tag.name) for tag in TipoCampo], required=True)
    descrizione=forms.CharField(widget=forms.Textarea,label="Descrizione")
    sinonimi=forms.CharField(label="Sinonimi",required=False)