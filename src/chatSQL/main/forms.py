from django import forms
from admin.models import StrutturaDatabase

class NLPromptForm(forms.Form):
    natural_language = forms.CharField(label='Frase in linguaggio naturale', widget=forms.Textarea)
    db_structure = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label='Struttura Database')
    
class QueryForm(forms.Form):
    prompt = forms.CharField(label='Prompt', widget=forms.HiddenInput)