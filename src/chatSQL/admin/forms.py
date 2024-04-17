from django import forms
from .enums import TipoCampo

# necessario per TabellaForm::struttura
# from .models import StrutturaDatabase

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
class StrutturaDatabaseForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    
class TabellaForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    sinonimi = forms.CharField(required=False, label="Sinonimi")
    # rimosso perché fk presa da url
    # struttura = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label="struttura_db")
    
class EliminaForm(forms.Form):
    classe_modello = forms.CharField(widget=forms.HiddenInput)
    id_modello = forms.IntegerField(widget=forms.HiddenInput)

class CampoTabella(forms.Form):
    nome=forms.CharField(label="Nome")
    tipo=forms.ChoiceField(choices=[(tag.value, tag.name) for tag in TipoCampo], required=True, label="Tipo")
    descrizione=forms.CharField(widget=forms.Textarea,label="Descrizione")
    sinonimi=forms.CharField(label="Sinonimi",required=False)