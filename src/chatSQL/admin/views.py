from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth import login,authenticate,logout

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


class AdminLogoutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('admin_login')
        
        messages.error(request,"Impossibile effettuare il logout.")
        return redirect('admin_login')      


class AdminHomeView(View):
    def get(self,request):
        strutture_db = models.StrutturaDatabase.objects.order_by("nome")
        return render(request,'admin/home.html',{'strutture_db':strutture_db})


class AdminStrutturaDatabaseView(View):
    
    def get(self, request,structure_id=None):
        
        if structure_id is not None: # la view mostra il form pre-compilato per la modifica
            struttura = models.StrutturaDatabase.objects.get(pk=structure_id)
            db_create_form = forms.StrutturaDatabaseForm(initial={'nome':struttura.nome,'descrizione':struttura.descrizione})
            return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
    
        db_create_form = forms.StrutturaDatabaseForm #mostra il form vuoto per l'inserimento
        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})

    def post(self, request,structure_id=None):
        db_create_form = forms.StrutturaDatabaseForm(request.POST)
        
        if db_create_form.is_valid():
            try:
                
                nome        = db_create_form.cleaned_data['nome']
                descrizione = db_create_form.cleaned_data['descrizione']
                
                if structure_id is not None:
                    
                    if models.StrutturaDatabase.objects.filter(nome=nome).filter(~Q(pk=structure_id)).exists():
                        db_create_form.add_error('nome', 'Un database con questo nome è già esistente.')
                        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
                    
                    db_structure = models.StrutturaDatabase.objects.get(pk=structure_id)
                    db_structure.nome = nome
                    db_structure.descrizione = descrizione
                    db_structure.save()
                    
                    db_create_form = forms.StrutturaDatabaseForm(initial={'nome':db_structure.nome,'descrizione':db_structure.descrizione})
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})

                    
                
                if models.StrutturaDatabase.objects.filter(nome=nome).exists():
                    db_create_form.add_error('nome', 'Un database con questo nome è già esistente.')
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
                
                db_structure = models.StrutturaDatabase(nome=nome, descrizione=descrizione)
                db_structure.save()
                messages.add_message(request, messages.SUCCESS, 'Struttura creata con successo')
                
                return redirect('db_view',db_structure.id)
            
            except Exception as e:
                error_message = str(e)
                messages.add_message(request, messages.ERROR, 'Errore durante il salvataggio della struttura: ' + error_message)
                return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})
        
        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form})