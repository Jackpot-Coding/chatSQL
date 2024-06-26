from django.shortcuts import render
from django.views import View

from django.contrib import messages

from . import forms

from .prompt_creator import PromptCreator
from .enums import PromptGenStatus
from .query_generator import QueryGenerator


import markdown
# Create your views here.

main_template = "main.html"

class MainView(View):
    def get(self,request):       
        natural_lang_form = forms.NLPromptForm()
        return render(request,"main.html", {"natural_lang_form":natural_lang_form})
    
    def post(self,request):
        
        natural_lang_form = forms.NLPromptForm(request.POST)

        if not natural_lang_form.is_valid():
            messages.add_message(request,messages.ERROR,"Errore nel form.")
            return render(request,main_template,  {"natural_lang_form":natural_lang_form})
        
        natural_language_request = natural_lang_form.cleaned_data["natural_language"]
        db_structure = natural_lang_form.cleaned_data["db_structure"]
        
        generator = PromptCreator(db_structure)
        
        prompt = generator.create_prompt(natural_language_request)
        
        if prompt[0] != PromptGenStatus.SUCCESS:
            messages.add_message(request,messages.ERROR,prompt[1])
            return render(request,main_template,  {"natural_lang_form":natural_lang_form})
        
        query_form = forms.QueryForm(initial={"prompt":prompt[1]})    
            
        return render(request,main_template,  {"natural_lang_form":natural_lang_form, "prompt":prompt[1],'query_form':query_form})
    
class QueryGenerationView(View):
    
    def post(self,request):
        
        query_form = forms.QueryForm(request.POST)
        natural_lang_form = forms.NLPromptForm()
        
        if query_form.is_valid():
            
            prompt = query_form.cleaned_data['prompt']              
                
            query_generator = QueryGenerator()
            query = query_generator.get_query(prompt)
                
            if query == 'interpretation':                        
                messages.error(request,"Errore di interpretazione del prompt.")
                return render(request,main_template,  {"natural_lang_form":natural_lang_form})  
            
            if query == 'error':
                messages.error(request,"Errore di comunicazione con servizio di generazione query.")
                return render(request,main_template,  {"natural_lang_form":natural_lang_form})  
            
            md = markdown.Markdown(extensions=["fenced_code"])
            
            return render(request,"query.html",{"query":md.convert(query) })
                    
        
        messages.error(request,"Prompt non fornito.")
        return render(request,main_template,  {"natural_lang_form":natural_lang_form}) 