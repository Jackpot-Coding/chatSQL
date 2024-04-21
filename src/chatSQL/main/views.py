from django.shortcuts import render
from django.views import View

from django.contrib import messages

from . import forms
from admin.models import StrutturaDatabase
from .prompt_creator import PromptCreator
from .enums import PromptGenStatus

# Create your views here.

class NaturalLanguageView(View):
    def get(self,request):
        natural_lang_form = forms.NaturalLanguageForm
        return render(request,"natural_language.html", {"natural_lang_form":natural_lang_form})
    
    def post(self,request):
        
        natural_lang_form = forms.NaturalLanguageForm(request.POST)

        if not natural_lang_form.is_valid():
            messages.add_message(request,messages.ERROR,"Errore nel form.")
            return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form})
        
        natural_language_request = natural_lang_form.cleaned_data["natural_language"]
        db_structure = natural_lang_form.cleaned_data["db_structure"]

        if (db_structure is None):
            messages.add_message(request,messages.ERROR,"Struttura DataBase non selezionata.")
            return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form})
        
        if (natural_language_request == ""):
            messages.add_message(request,messages.ERROR,"Prompt vuoto.")
            return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form}) 
        
        generator = PromptCreator(db_structure)
        
        promt = generator.createPrompt(natural_language_request)
        
        if promt[0] != PromptGenStatus.SUCCESS:
            messages.add_message(request,messages.ERROR,promt[1])
            return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form})
            
        return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form, "prompt_form":promt[1]})