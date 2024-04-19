from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from ..forms import EliminaForm
from ..models import StrutturaDatabase, Tabella, Campo

class adminTestCase(TestCase):
    
    client = Client
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        
        struttura_db = StrutturaDatabase(nome="Test DB",descrizione="Descrizione test")
        struttura_db.save()
        tab_test = Tabella(nome="Test Tabella", descrizione="Descrizione test", struttura=struttura_db)
        tab_test.save()
        campo = Campo(nome="Test Tabella", tipo="INT", descrizione="Descrizione test", tabella=tab_test)
        campo.save()
    
    def test_can_render_struttura_database_deletion_form(self):
        
        response = self.client.get(reverse("model_delete",kwargs={"classe_modello":"StrutturaDatabase","id_modello":1}))
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/delete.html')
        self.assertContains(response,'value="StrutturaDatabase"')
        self.assertContains(response,'value="1"')
    
    def test_can_delete_struttura_database(self):
        url = reverse("model_delete",kwargs={"classe_modello":"StrutturaDatabase","id_modello":1})
        response = self.client.post(url,data={"classe_modello":"StrutturaDatabase","id_modello":"1"})
        
        messages = [msg for msg in get_messages(response.wsgi_request)]
        
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('admin_home'))
        self.assertTrue("Struttura database eliminata" in messages[0].message)

    def test_can_delete_tabella(self):
        url = reverse("model_delete",kwargs={"classe_modello":"Tabella","id_modello":1})
        response = self.client.post(url,data={"classe_modello":"Tabella","id_modello":"1"})

        messages = [msg for msg in get_messages(response.wsgi_request)]

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("db_view", kwargs={'structure_id':1}))
        self.assertTrue("Tabella eliminata" in messages[0].message)

    def test_can_delete_campo(self):
        url = reverse("model_delete",kwargs={"classe_modello":"Campo","id_modello":1})
        response = self.client.post(url,data={"classe_modello":"Campo","id_modello":"1"})

        messages = [msg for msg in get_messages(response.wsgi_request)]

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("table_view", kwargs={'table_id':1}))
        self.assertTrue("Campo eliminato" in messages[0].message)
        
    def test_cannot_delete_not_existing_struttura_database(self):
        url = reverse("model_delete",kwargs={"classe_modello":"StrutturaDatabase","id_modello":100})
        response = self.client.post(url,data={"classe_modello":"StrutturaDatabase","id_modello":"100"})
        
        messages = [msg for msg in get_messages(response.wsgi_request)]
        
        self.assertEqual(response.status_code,302) #fa redirect alla pagina precedente
        self.assertTrue("Errore durante la richiesta di eliminazione" in messages[0].message)
        
    def test_cannot_delete_not_existing_model_class(self):
        url = reverse("model_delete",kwargs={"classe_modello":"NotExistingModel","id_modello":100})
        response = self.client.post(url,data={"classe_modello":"NotExistingModel","id_modello":"100"})
        
        messages = [msg for msg in get_messages(response.wsgi_request)]
        
        self.assertEqual(response.status_code,302) #fa redirect alla pagina precedente
        self.assertTrue("Errore durante la richiesta di eliminazione" in messages[0].message)
            