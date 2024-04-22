from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth import login,authenticate,logout

from django.contrib import messages

from . import forms
from . import models
from . import file_uploader
from . import enums

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
                    return render(request,"admin/home.html",{"login_form":login_form})
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
            return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,
                                                            'editing_id':structure_id,
                                                            'struttura_nome':struttura.nome, 
                                                            'tables':struttura.tabella_set.all()})
    
        db_create_form = forms.StrutturaDatabaseForm #mostra il form vuoto per l'inserimento
        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'struttura_nome':'Nuova struttura'})

    def post(self, request,structure_id=None):
        db_create_form = forms.StrutturaDatabaseForm(request.POST)
        
        if db_create_form.is_valid():
            try:
                
                nome        = db_create_form.cleaned_data['nome']
                descrizione = db_create_form.cleaned_data['descrizione']
                
                if structure_id is not None:
                    db_structure=models.StrutturaDatabase.objects.get(pk=structure_id)
                    if models.StrutturaDatabase.objects.filter(nome=nome).filter(~Q(pk=structure_id)).exists():
                        db_create_form.add_error('nome', 'Un database con questo nome è già esistente.')
                        return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'editing_id':structure_id,
                                                                            'struttura_nome':db_structure.nome})
                    
                    db_structure.nome = nome
                    db_structure.descrizione = descrizione
                    db_structure.save()
                    
                    db_create_form = forms.StrutturaDatabaseForm(initial={'nome':db_structure.nome,'descrizione':db_structure.descrizione})
                    messages.add_message(request, messages.SUCCESS, 'Struttura modificata con successo')
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'editing_id':structure_id, 
                                                                        'tables':db_structure.tabella_set.all()})

                    
                
                if models.StrutturaDatabase.objects.filter(nome=nome).exists():
                    db_create_form.add_error('nome', 'Un database con questo nome è già esistente.')
                    return render(request, 'admin/struttura_db.html', {'db_create_form': db_create_form,'struttura_nome':'Nuova struttura'})
                
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
                
                if classe_modello == 'Tabella':
                    oggetto = models.Tabella.objects.get(pk=int(id_modello))
                    db = oggetto.struttura.pk
                    oggetto.delete()
                    messages.success(request, "Tabella eliminata")
                    #return redirect("../../struttureDB/"+str(db))
                    return redirect("db_view", db)

                if classe_modello == 'Campo':
                    oggetto = models.Campo.objects.get(pk=int(id_modello))
                    tab = oggetto.tabella.pk
                    oggetto.delete()
                    messages.success(request, "Campo eliminato")
                    #return redirect("../../tabella/"+str(tab))
                    return redirect("table_view", tab)
            
                #se non trova una classe esplicitatamente abilitata
                messages.error(request,"Errore durante la richiesta di eliminazione")
                return redirect(request.get_full_path()) #ritorna l'url precedente

            #else non serve perchè l'url per forza ha i due parametri o va in errore 404 ma va messo in caso
            messages.error(request,"Errore durante la richiesta di eliminazione")
            return redirect(request.get_full_path()) #ritorna l'url precedente

        except Exception: #se non esiste il modello con id dato e la query non è valida
            
            messages.error(request,"Errore durante la richiesta di eliminazione")
            return redirect(request.get_full_path()) #ritorna l'url precedente

class AdminTabellaView(View):
    
    def get(self,request,structure_id=None, table_id=None):
        
        try:
        
            if structure_id is not None:
                                
                # In caso di crea tabella
                struttura_db = models.StrutturaDatabase.objects.get(pk=structure_id)
                table_create_form = forms.TabellaForm
                return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 
                                                            'structure_id': structure_id,'struttura_db':struttura_db})
            
            if table_id is not None:
                table = models.Tabella.objects.get(pk = table_id)
                struttura_db = table.struttura
                table_create_form = forms.TabellaForm(initial={'nome':table.nome,'descrizione':table.descrizione,'sinonimi':table.sinonimi})
                return render(request, 'admin/tabella.html', {'table_create_form': table_create_form,'structure_id':struttura_db.id, 
                                                            'struttura_db':struttura_db, 
                                                            'table_id': table_id,"table":table, 'fields': table.campo_set.all()})

            # else: sto visualizzando una tabella, non può essere senza tabella id
            messages.error(request,"Tabella non trovata.")
            return redirect('admin_home') 
        
        except Exception:
            messages.error(request,"Tabella non trovata.")
            return redirect('admin_home') 
    
    def post(self,request,structure_id=None, table_id=None): # table_id = None per eventuale visualizza/modifica
    
        table_create_form = forms.TabellaForm(request.POST)
        
        if table_create_form.is_valid():
            try:
                nome = table_create_form.cleaned_data['nome']
                descrizione = table_create_form.cleaned_data['descrizione']
                sinonimi = table_create_form.cleaned_data['sinonimi']
                # sinonimi = (create_table.cleaned_data["sinonimi"]).split(", ") in caso in futuro si voglia salvare i sinonimi come array

                if table_id is None: # creazione
                    db_structure = models.StrutturaDatabase.objects.get(pk=structure_id)
                    if db_structure.tabella_set.filter(nome=nome).exists():
                        messages.add_message(request, messages.ERROR, 'Una tabella con questo nome è già esistente.')
                        return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 
                                                                        'structure_id': structure_id,'struttura_db':db_structure})
                    
                    table = models.Tabella(
                        nome = nome,
                        descrizione = descrizione,
                        sinonimi = sinonimi,
                        struttura = db_structure
                    )
                    table.save()
                    messages.add_message(request, messages.SUCCESS, 'Tabella creata con successo')
                    return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 'structure_id': structure_id,
                                                                'struttura_db':db_structure, 'table_id':table.pk})
                
                # modifica/visualizza
                table = models.Tabella.objects.get(pk=table_id)
                if table.nome != nome:  # Controllo solo se il nome viene modificato
                    if table.struttura.tabella_set.filter(nome=nome).exists():
                        messages.error(request, 'Una tabella con questo nome è già esistente.')
                        return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 
                                                                    'structure_id': structure_id, 'struttura_db':table.struttura, 'table_id': table_id})
                
                table.nome = nome
                table.descrizione = descrizione
                table.sinonimi = sinonimi
                table.save()
                messages.add_message(request, messages.SUCCESS, 'Tabella modificata con successo')
                return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 'struttura_db':table.struttura,
                                                            'structure_id': structure_id, 'table_id':table.pk, 'fields': table.campo_set.all()})
                
            except Exception as e:
                error_message = str(e)
                db_structure = models.StrutturaDatabase.objects.get(pk=structure_id)
                messages.add_message(request, messages.ERROR, 'Errore durante il salvataggio della tabella: ' + error_message)
                return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 'structure_id': structure_id,
                                                            'struttura_db':db_structure})
        else:
            db_structure = models.StrutturaDatabase.objects.get(pk=structure_id)
            messages.add_message(request, messages.ERROR, 'Il form non è valido.')
            return render(request, 'admin/tabella.html', {'table_create_form': table_create_form, 
                                                        'structure_id': structure_id,'struttura_db':db_structure})


class AdminCampoView(View):
    def get(self,request,table_id=None,field_id=None):
        if field_id is not None:
            if not models.Campo.objects.filter(pk=field_id).exists():
                messages.add_message(request, messages.ERROR, 'Il campo selezionato non esiste.')
                return render(request, 'admin/base.html')
            field=models.Campo.objects.get(pk=field_id)
            field_create_form=forms.CampoForm(initial={'nome':field.nome,'tipo':field.tipo,'descrizione':field.descrizione,'sinonimi':field.sinonimi})
            return  render(request, 'admin/campo.html', {'field_create_form': field_create_form,
                                                            'struttura':field.tabella.struttura,
                                                            'tabella':field.tabella,
                                                            'campo_nome':field.nome})
        field_create_form=forms.CampoForm
        if not models.Tabella.objects.filter(pk=table_id).exists():
            messages.add_message(request, messages.ERROR, 'La tabella selezionata non esiste.')
            return render(request, 'admin/base.html')
        return render(request, 'admin/campo.html', {'field_create_form': field_create_form,
                                                    'struttura':models.Tabella.objects.get(pk=table_id).struttura,
                                                    'tabella':models.Tabella.objects.get(pk=table_id),
                                                    'campo_nome':'Nuovo campo'})

    def post(self,request,table_id=None,field_id=None):
        field_create_form=forms.CampoForm(request.POST)
        if field_create_form.is_valid():
            try:
                nome=field_create_form.cleaned_data['nome']
                tipo=field_create_form.cleaned_data['tipo']
                descrizione=field_create_form.cleaned_data['descrizione']
                sinonimi=field_create_form.cleaned_data['sinonimi']

                if field_id is not None:

                    table=models.Campo.objects.get(pk=field_id).tabella
                    
                    if table.campo_set.filter(nome=nome).filter(~Q(pk=field_id)).exists():
                        field_create_form.add_error('nome', 'Un campo con questo nome è già esistente.')
                        return render(request, 'admin/campo.html', {'field_create_form': field_create_form,
                                                                    'struttura':table.struttura,
                                                                    'tabella':table,
                                                                    'campo_nome':table.campo_set.get(pk=field_id).nome})
                    
                    field=models.Campo.objects.get(pk=field_id)
                    field.nome=nome
                    field.tipo=tipo
                    field.descrizione=descrizione
                    field.sinonimi=sinonimi
                    field.save()
                    field_create_form=forms.CampoForm(initial={'nome':field.nome,
                                                                    'tipo':field.tipo,
                                                                    'descrizione':field.descrizione,
                                                                    'sinonimi':field.sinonimi})
                    return  render(request, 'admin/campo.html', {'field_create_form': field_create_form,
                                                                'struttura':table.struttura,
                                                                'tabella':table,
                                                                'campo_nome':table.campo_set.get(pk=field_id).nome})
                
                table=models.Tabella.objects.get(pk=table_id)
                if table.campo_set.filter(nome=nome).exists():
                    field_create_form.add_error('nome', 'Un campo con questo nome è già esistente.')
                    return render(request, 'admin/campo.html', {'field_create_form': field_create_form,
                                                                'struttura':table.struttura,
                                                                'tabella':table,
                                                                'campo_nome':'Nuovo campo'})
                
                field=table.campo_set.create(nome=nome,tipo=tipo,descrizione=descrizione,sinonimi=sinonimi)
                messages.add_message(request, messages.SUCCESS, 'Campo creato con successo')
                
                return redirect('campo_view',field.id)
                
            except Exception as e:
                error_message = str(e)
                messages.add_message(request, messages.ERROR, 'Errore durante il salvataggio del campo: ' + error_message)
                return render(request, 'admin/campo.html', {'field_create_form': field_create_form})
        
        return render(request, 'admin/campo.html', {'field_create_form': field_create_form})
    
class AdminUploadFileView(View):
    def get(self,request):
        upload_file_form=forms.UploadFileForm()
        return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})

    def post(self,request):
        upload_file_form=forms.UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            try:
                file=request.FILES['file']
            except Exception as e:
                error_message = str(e)
                messages.add_message(request, messages.ERROR, 'Errore durante il caricamento del file: ' + error_message)
                return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})
        else:
            messages.add_message(request, messages.ERROR, 'Il form non è valido.')
            return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})
        
        uploader = file_uploader.FileUploader(file)
        if uploader.getStatus() is not None:
            messages.add_message(request, messages.ERROR, 'Errore durante l\'upload del file: ' + uploader.getStatus())
            return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})
        status = uploader.uploadFile()
        if status[0] != enums.ParserStatus.SUCCESS:
            messages.add_message(request, messages.ERROR, 'Errore durante l\'upload del file: ' + status[1])
            return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})
        return render(request, 'admin/upload_file.html', {'upload_file_form': upload_file_form})