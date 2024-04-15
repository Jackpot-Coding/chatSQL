from django.shortcuts import render
from django.views import View

from . import forms

# Create your views here.

class PromptView(View):
    def get(self,request):
        promt_form = forms.PromptForm
        return render(request,"prompt.html", {"prompt_form":promt_form})
    
    def post(self,request):
        promt_form = forms.PromptForm(request.POST)
        return render(request,"prompt.html",  {"prompt_form":promt_form})