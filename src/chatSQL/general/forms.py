from django import forms
from admin.models import StrutturaDatabase

class PromptForm(forms.Form):
    free_text = forms.CharField(label='Prompt', widget=forms.Textarea)
    structure = forms.ModelChoiceField(queryset=StrutturaDatabase.objects.all(), label='Database Structure')