from django.shortcuts import render
from django.views import View

from django.contrib.auth import login,logout,authenticate

from django.contrib import messages

from . import forms

class AdminLoginView(View):
   def get(self,request):
      login_form = forms.LoginForm
      return render(request,"admin/login.html",{"login_form":login_form})
   
   def post(self,request):
      login_form = forms.LoginForm(request.POST)
      if login_form.is_valid():
         try:
            user = authenticate(username=login_form.cleaned_data["username"],password=login_form.cleaned_data["password"])
            if user is not None :
               login(request,user)
               messages.add_message(request,messages.SUCCESS,"Autenticazione avvenuta con successo")
               return render(request,"admin/login.html",{"login_form":login_form})
            else:
               login_form.add_error("username","Credenziali non corrette.")
               return render(request,"admin/login.html",{"login_form":login_form})
         except Exception:
            messages.add_message(request,messages.ERROR,"Errore durante l'autenticazione.")
            return render(request,"admin/login.html",{"login_form":login_form}) 