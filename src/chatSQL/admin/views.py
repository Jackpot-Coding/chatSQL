from django.shortcuts import render
from django.views import View

from django.contrib.auth import login,logout,authenticate

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
               return render(request,"admin/login.html",{"message":"OK","login_form":login_form})
            else:
               login_form.add_error("username","Credenziali non corrette")
               return render(request,"admin/login.html",{"login_form":login_form})
         except Exception:
            return render(request,"admin/login.html",{"message":"Errore auth","login_form":login_form}) 