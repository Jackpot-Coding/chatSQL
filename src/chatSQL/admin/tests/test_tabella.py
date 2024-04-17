from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import TabellaForm
from ..models import Tabella
from ..models import StrutturaDatabase

class CreateTableTestCase(TestCase):
    client = Client() # client per eseguire get e post
    db = StrutturaDatabase(nome='Test Str', descrizione='Test Db Descrizione') # db di test
    
    def setUp(self):
        User.objects.create_user(username="testAdmin", password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        self.db.save() # salva il db
        
    def test_can_reach_table_creation_page(self):
        # passa come argomento la pk del db
        response = self.client.get(reverse('new_table_view', args=(self.db.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/tabella.html')
        
    def test_can_create_table(self):
        
        data = {'nome': 'Test Table', 
                'descrizione': 'Test Table Description', 
                'sinonimi': 'Test Sinonimi', 
            }                                   # passa come argomento la pk del db alla post, e i dati mancanti per creare la tabella
        response = self.client.post(reverse('new_table_view', args=(self.db.pk,)), data)
        self.assertEqual(response.status_code, 200) #tabella creata
        self.assertTrue(Tabella.objects.filter(nome='Test Table').exists()) # tabella corretta
        
#class TabellaFormTestCase(TestCase):
    