from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth import login,authenticate

from django.contrib import messages

from . import forms
from . import models

from django.db.models import Q


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

class AdminHomeView(View):
    def get(self,request):
        strutture_db = models.StrutturaDatabase.objects.order_by("name")
        return render(request,'admin/home.html',{'strutture_db':strutture_db})


class AdminStrutturaDatabaseView(View):
    def get(self, request,id=None):
        
        if id: # la view mostra il form pre-compilato per la modifica
            struttura = models.StrutturaDatabase.objects.get(pk=id)
            db_create_form = forms.StrutturaDatabaseForm(initial={'name':struttura.name,'description':struttura.description})
            return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
    
        db_create_form = forms.StrutturaDatabaseForm #mostra il form vuoto per l'inserimento
        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})

    def post(self, request,id=None):
        db_create_form = forms.StrutturaDatabaseForm(request.POST)
        if db_create_form.is_valid():
            try:
                
                name        = db_create_form.cleaned_data['name']
                description = db_create_form.cleaned_data['description']
                
                if id:
                    
                    if models.StrutturaDatabase.objects.filter(name=name).filter(~Q(pk=id)).exists():
                        db_create_form.add_error('name', 'Un database con questo nome è già esistente.')
                        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
                    
                    db_structure = models.StrutturaDatabase.objects.get(pk=id)
                    db_structure.name = name
                    db_structure.description = description
                    db_structure.save()
                    
                    db_create_form = forms.StrutturaDatabaseForm(initial={'name':db_structure.name,'description':db_structure.description})
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})

                    
                
                if models.StrutturaDatabase.objects.filter(name=name).exists():
                    db_create_form.add_error('name', 'Un database con questo nome è già esistente.')
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
                
                db_structure = models.StrutturaDatabase(name=name, description=description)
                db_structure.save()
                messages.add_message(request, messages.SUCCESS, 'Struttura creata con successo')
                
                return redirect('db_view',db_structure.id)
            
            except Exception as e:
                error_message = str(e)
                messages.add_message(request, messages.ERROR, 'Errore durante la creazione della struttura: ' + error_message)
                return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
        
        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})

