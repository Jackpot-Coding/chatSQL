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
            return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'editing_id':structure_id, 'tables':struttura.tabella_set.all()})
    
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
                        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'editing_id':structure_id})
                    
                    db_structure = models.StrutturaDatabase.objects.get(pk=structure_id)
                    db_structure.nome = nome
                    db_structure.descrizione = descrizione
                    db_structure.save()
                    
                    db_create_form = forms.StrutturaDatabaseForm(initial={'nome':db_structure.nome,'descrizione':db_structure.descrizione})
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'editing_id':structure_id})

                    
                
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
    
class AdminEliminaModelView(View):
    
    def get(self,request,classe_modello=None,id_modello=None):
        
        elimina_form = forms.EliminaForm(initial={'id_modello':id_modello,'classe_modello':classe_modello})
        return render(request,"admin/delete.html",{"elimina_form":elimina_form,'classe_modello':classe_modello,'id_modello':id_modello})
    
    def post(self,request,classe_modello=None,id_modello=None):
        elimina_form = forms.EliminaForm(request.POST)

        try:
            
            if elimina_form.is_valid():
                
                classe_modello = elimina_form.cleaned_data['classe_modello']
                id_modello     = elimina_form.cleaned_data['id_modello']
                
                if classe_modello == 'StrutturaDatabase':
                    
                    oggetto = models.StrutturaDatabase.objects.get(pk=int(id_modello))
                    oggetto.delete()
                    messages.success(request,"Struttura database eliminata.")
                    return redirect("admin_home")
            
                #se non trova una classe esplicitatamente abilitata
                messages.error(request,"Errore durante la richiesta di eliminazione")
                return redirect(request.get_full_path()) #ritorna l'url precedente

            #else non serve perchè l'url per forza ha i due parametri o va in errore 404 ma va messo in caso
            messages.error(request,"Errore durante la richiesta di eliminazione")
            return redirect(request.get_full_path()) #ritorna l'url precedente

        except Exception: #se non esiste il modello con id dato e la query non è valida
            
            messages.error(request,"Errore durante la richiesta di eliminazione")
            return redirect(request.get_full_path()) #ritorna l'url precedente
            
            
class AdminCreaTabellaView(View):
    def get(self, request, structure_id):
        create_table = forms.TabellaForm
        return render(request, 'admin/tabella.html', {'create_table': create_table, 'structure_id': structure_id})
    
    def post(self, request, structure_id):
        
        # raccoglie dati dal form
        create_table = forms.TabellaForm(request.POST)
        
        # controlla che siano validi, se true, li assegna ai rispettivi campi
        if create_table.is_valid():
            # assegnazione field
            nome = create_table.cleaned_data["nome"]
            descrizione = create_table.cleaned_data["descrizione"]
            # sinonimi = (create_table.cleaned_data["sinonimi"]).split(", ")
            sinonimi = create_table.cleaned_data["sinonimi"]
            struttura = models.StrutturaDatabase.objects.get(pk = structure_id)
            
            # creazione oggetto tabella
            table = models.Tabella(
                nome = nome, 
                descrizione = descrizione, 
                sinonimi = sinonimi, 
                struttura = struttura
            )
            # save tabella creata e messaggio
            table.save()
            messages.add_message(request, messages.SUCCESS , "Tabella creata con successo")
        
        return render(request, 'admin/tabella.html', {'create_table': create_table})
            
            