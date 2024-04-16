from django import forms

# necessario per TabellaForm::struttura
#from models import StrutturaDatabase

class LoginForm(forms.Form):
    username = forms.CharField(label="Nome Utente")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    
class StrutturaDatabaseForm(forms.Form):
    nome = forms.CharField(label="Nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="Descrizione")
    
class TabellaForm(forms.Form):
    nome = forms.CharField(max_length=255, required=True, label="nome")
    descrizione = forms.CharField(widget=forms.Textarea, label="descrizione")
    sinonimi = forms.CharField(max_length=255, required=False, label="sinonimi")
    #struttura = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label="struttura_db")    
    struttura = forms.CharField(max_length=255, required=True, label="struttura_db")    
    
    
class EliminaForm(forms.Form):
    classe_modello = forms.CharField(widget=forms.HiddenInput)
    id_modello = forms.IntegerField(widget=forms.HiddenInput)