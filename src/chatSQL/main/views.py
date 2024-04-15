from django.shortcuts import render
from django.views import View

from django.contrib import messages

from . import forms

# Create your views here.

class PromptView(View):
    def get(self,request):
        prompt_form = forms.PromptForm
        return render(request,"prompt.html", {"prompt_form":prompt_form})
    
    def post(self,request):
        prompt_form = forms.PromptForm(request.POST)

        if not prompt_form.is_valid():
            messages.add_message(request,messages.ERROR,"Errore nel form.")
            return render(request,"prompt.html",  {"prompt_form":prompt_form})
        
        natural_language = prompt_form.cleaned_data["natural_language"]
        db_structure = prompt_form.cleaned_data["db_structure"]

        if (db_structure is None):
            messages.add_message(request,messages.ERROR,"Struttura DataBase non selezionata.")
            return render(request,"prompt.html",  {"prompt_form":prompt_form})
        if (natural_language == ""):
            messages.add_message(request,messages.ERROR,"Prompt vuoto.")
            return render(request,"prompt.html",  {"prompt_form":prompt_form}) 
            
        return render(request,"prompt.html",  {"prompt_form":prompt_form})