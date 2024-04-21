from django.shortcuts import render
from django.views import View

from django.contrib import messages

from . import forms

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
        
        generator = PromptCreator(db_structure)
        
        prompt = generator.createPrompt(natural_language_request)
        
        if prompt[0] != PromptGenStatus.SUCCESS:
            messages.add_message(request,messages.ERROR,prompt[1])
            return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form})
            
        return render(request,"natural_language.html",  {"natural_lang_form":natural_lang_form, "prompt":prompt[1]})