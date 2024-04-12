from django.shortcuts import render
from django.views import View

from django.contrib.auth import login,authenticate

from django.contrib import messages

from . import forms
from . import models

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
                #else
                login_form.add_error("username","Credenziali non corrette.")
                return render(request,"admin/login.html",{"login_form":login_form})
            except Exception:
                messages.add_message(request,messages.ERROR,"Errore durante l'autenticazione.")
                return render(request,"admin/login.html",{"login_form":login_form}) 
        #else
        return render(request,"admin/login.html",{"login_form":login_form})
    
class CreateStructureView(View):
    def get(self, request):
        db_create_form = forms.DatabaseStructureForm
        return render(request, 'admin/db_creation.html', {'db_create_form': db_create_form})

    def post(self, request):
        db_create_form = forms.DatabaseStructureForm(request.POST)
        if db_create_form.is_valid():
            try:
                new_name = db_create_form.cleaned_data['name']
                description = db_create_form.cleaned_data['description']
                if models.DatabaseStructure.objects.filter(name=new_name).exists():
                    db_create_form.add_error('name', 'Un database con questo nome è già esistente.')
                    return render(request, 'admin/db_creation.html', {'db_create_form': db_create_form})
                else:
                    db_structure = models.DatabaseStructure(name=new_name, description=description)
                    db_structure.save()
                    messages.add_message(request, messages.SUCCESS, 'Struttura creata con successo')
                    return render(request, 'admin/db_creation.html', {'db_create_form': db_create_form})
            except Exception as e:
                error_message = str(e)
                messages.add_message(request, messages.ERROR, 'Errore durante la creazione della struttura: ' + error_message)
                return render(request, 'admin/db_creation.html', {'db_create_form': db_create_form})
        return render(request, 'admin/db_creation.html', {'db_create_form': db_create_form})
    
class DatabaseListView(View):
    def get(self, request):
        databases = models.DatabaseStructure.objects.all()
        return render(request, 'admin/db_list.html', {'databases': databases})