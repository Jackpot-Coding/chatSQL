from django import forms
from admin.models import StrutturaDatabase

class PromptForm(forms.Form):
    natural_language = forms.CharField(label='Prompt', widget=forms.Textarea)
    db_structure = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label='Database Structure')