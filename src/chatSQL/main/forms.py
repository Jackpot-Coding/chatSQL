from django import forms
from admin.models import StrutturaDatabase

class NLPromptForm(forms.Form):
    natural_language = forms.CharField(label='Natural Language', widget=forms.Textarea)
    db_structure = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label='Database Structure')
    
class PromptForm(forms.Form):
    prompt = forms.CharField(label='Prompt', widget=forms.HiddenInput)