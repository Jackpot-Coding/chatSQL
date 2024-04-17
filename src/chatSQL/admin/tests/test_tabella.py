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
    
    def test_invalid_form_create_table(self):
        data = {'nome': '', 'descrizione': 'Test Description', 'sinonimi': 'sinonimo'}
        response = self.client.post(reverse('new_table_view', args=(self.db.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tabella.objects.filter(nome='Test Table').exists())
    
    # def test errori tabella (doppio nome)
    
    ''' Per Marco Gobbo
        def modifica tabella:
        può raggiungere la pagina di modifica?
        nome già esistente 
        modifica non valida
        verifica modifica
    '''    
class TabellaFormTestCase(TestCase):

    def test_create_structure_invalid_name(self):
        data = {'nome': '', 'descrizione': 'Test Description', 'sinonimi': 'sinonimo'}
        self.assertFalse(TabellaForm(data).is_valid())
        
    def test_create_structure_invalid_description(self):
        data = {'nome': 'Test Tabella', 'descrizione': '', 'sinonimi': 'sinonimo'}
        self.assertFalse(TabellaForm(data).is_valid())
        
    def test_create_structure_invalid_synonymous(self):
        data = {'nome': 'Test Tabella', 'descrizione': 'Descrizione', 'sinonimi': ''}
        self.assertTrue(TabellaForm(data).is_valid()) # True perché può non avere sinonimi
    
    def test_create_structure_invalid_data(self):
        data = {'nome': '', 'descrizione': '', 'sinonimi': ''}
        self.assertFalse(TabellaForm(data).is_valid())
    