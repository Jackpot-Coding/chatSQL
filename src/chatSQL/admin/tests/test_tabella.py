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

    def test_create_table_duplicate_name(self):
        db = StrutturaDatabase.objects.create(nome="Test DB", descrizione="Description for test")
        db.tabella_set.create(nome="Test table", descrizione="Description for test", sinonimi="Synonyms for test")

        data = {'nome': 'Test table', 'descrizione': 'Description for test', 'sinonimi': 'Synonyms for test'}
        response = self.client.post(reverse('new_table_view', args=(db.pk,)), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Una tabella con questo nome è già esistente.')
        self.assertFalse(Tabella.objects.filter(nome='Test Table').exists())

    def test_can_reach_table_edit_page(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        response = self.client.get(reverse("table_view",args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/tabella.html')

    def test_cannot_edit_table_with_other_existing_name(self):
        db = StrutturaDatabase.objects.create(nome="Test DB", descrizione="Description for test")
        db.tabella_set.create(nome="Test table1", descrizione="Description for test", sinonimi="Synonyms for test")
        db.tabella_set.create(nome="Test table2", descrizione="Description for test", sinonimi="Synonyms for test")

        data = {'nome': 'Test table1', 'descrizione': 'Description for test', 'sinonimi': 'Synonyms for test'}
        response = self.client.post(reverse('table_view', args=(2,)), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/tabella.html')
        self.assertContains(response, 'Una tabella con questo nome è già esistente.')
        self.assertFalse(Tabella.objects.filter(nome='Test Table').exists())

    def test_can_edit_table(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()

        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        data={'nome':'Test table edited','descrizione':'Description for test edited','sinonimi':'Synonyms for test edited'}
        response=self.client.post(reverse('table_view',args=(1,)),data)
        editedTable=Tabella.objects.get(pk=1)

        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Test table edited')
        self.assertContains(response,'Description for test edited')
        self.assertContains(response,'Synonyms for test edited')
        self.assertEqual(editedTable.nome,'Test table edited')
        self.assertEqual(editedTable.descrizione,'Description for test edited')
        self.assertEqual(editedTable.sinonimi,'Synonyms for test edited')
        self.assertTemplateUsed(response,'admin/tabella.html')
        
    def test_error_with_not_existing_table(self):
        response = self.client.get(reverse("table_view",args=(10000,)))
        
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('admin_home'))
    
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
    