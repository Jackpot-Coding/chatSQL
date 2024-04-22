from django.shortcuts import render
from django.views import View

from django.contrib import messages

from . import forms

from .prompt_creator import PromptCreator
from .enums import PromptGenStatus
from .query_generator import QueryGenerator


import markdown2

# Create your views here.

class MainView(View):
    def get(self,request):       
        natural_lang_form = forms.NLPromptForm()
        return render(request,"main.html", {"natural_lang_form":natural_lang_form})
    
    def post(self,request):
        
        natural_lang_form = forms.NLPromptForm(request.POST)

        if not natural_lang_form.is_valid():
            messages.add_message(request,messages.ERROR,"Errore nel form.")
            return render(request,"main.html",  {"natural_lang_form":natural_lang_form})
        
        natural_language_request = natural_lang_form.cleaned_data["natural_language"]
        db_structure = natural_lang_form.cleaned_data["db_structure"]
        
        generator = PromptCreator(db_structure)
        
        prompt = generator.createPrompt(natural_language_request)
        
        if prompt[0] != PromptGenStatus.SUCCESS:
            messages.add_message(request,messages.ERROR,prompt[1])
            return render(request,"main.html",  {"natural_lang_form":natural_lang_form})
        
        prompt_form = forms.PromptForm(initial={"prompt":prompt[1]})    
            
        return render(request,"main.html",  {"natural_lang_form":natural_lang_form, "prompt":prompt[1],'prompt_form':prompt_form})
    
class QueryGenerationView(View):
    
    def post(self,request):
        
        prompt_form = forms.PromptForm(request.POST)
        natural_lang_form = forms.NLPromptForm()
        
        if prompt_form.is_valid():
            
                prompt = prompt_form.cleaned_data['prompt']              
                
                query_generator = QueryGenerator()
                query = query_generator.getQuery(prompt)
                
                if query == 'interpretation':                        
                    messages.error(request,"Errore di interpretazione del prompt.")
                    return render(request,"main.html",  {"natural_lang_form":natural_lang_form})  
                
                elif query == 'error':
                    messages.error(request,"Errore di comunicazione con servizio di generazione query.")
                    return render(request,"main.html",  {"natural_lang_form":natural_lang_form})  
                
                else:
                    return render(request,"query.html",{"query":markdown2.markdown(query) })
                    
        
        messages.error(request,"Prompt non fornito.")
        return render(request,"main.html",  {"natural_lang_form":natural_lang_form}) 