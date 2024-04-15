from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import StrutturaDatabaseForm
from ..models import StrutturaDatabase

class createStructureTestCase(TestCase):
    
    client = Client()
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')


    def test_can_reach_structure_creation_page(self):
        response = self.client.get(reverse('new_db_view'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/struttura_db.html')


    def test_can_create_structure(self):
        data = {'nome': 'Test Database', 'descrizione': 'Test Description'}
        response = self.client.post(reverse('new_db_view'), data)
        
        self.assertEqual(response.status_code, 302) #redirect a struttura creata
        self.assertTrue(StrutturaDatabase.objects.filter(nome='Test Database').exists())
        
    def test_invalid_form_for_structure_creation(self):
        data = {'nome': '', 'descrizione': ''}
        response = self.client.post(reverse('new_db_view'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/struttura_db.html')
        
    def test_create_structure_duplicate_name(self):
        StrutturaDatabase.objects.create(nome='Existing Database', descrizione='Existing Description')
        
        data = {'nome': 'Existing Database', 'descrizione': 'Test Description'}
        response = self.client.post(reverse('new_db_view'), data)
        
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Un database con questo nome è già esistente.')
        self.assertFalse(StrutturaDatabase.objects.filter(nome='Test Database').exists())
        
    def test_can_reach_structure_edit_page(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        response = self.client.get(reverse("db_view",args=(1,)))
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/struttura_db.html')
    
    def test_cannot_edit_structure_with_other_existing_name(self):
        db1 = StrutturaDatabase(nome="Test DB1",descrizione="Description for test1")
        db1.save()
        
        db2 = StrutturaDatabase(nome="Test DB2",descrizione="Description for test2")
        db2.save()
        
        data = {"nome":"Test DB1","descrizione":"Description for bad name"}
        response = self.client.post(reverse('db_view',args=(2,)),data)
        
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'Un database con questo nome è già esistente.')
        self.assertTemplateUsed(response,'admin/struttura_db.html')
        
    def test_can_edit_structure(self):
        db1 = StrutturaDatabase(nome="Test DB1",descrizione="Description for test1")
        db1.save()
        
        data = {"nome":"Edited Name","descrizione":"Edited Description"}
        response = self.client.post(reverse('db_view',args=(1,)),data)
        
        editedDb = StrutturaDatabase.objects.get(pk=1)
        
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'Edited Name')
        self.assertContains(response, 'Edited Description')
        self.assertEqual(editedDb.nome,"Edited Name")
        self.assertEqual(editedDb.descrizione,"Edited Description")
        self.assertTemplateUsed(response,'admin/struttura_db.html')
        
        

class StrutturaDatabaseFormTestCase(TestCase):

    def test_create_structure_invalid_name(self):
        data = {'nome': '', 'descrizione': 'Test Description'}
        self.assertFalse(StrutturaDatabaseForm(data).is_valid())
        
    def test_create_structure_invalid_description(self):
        data = {'nome': 'Test Database', 'descrizione': ''}
        self.assertFalse(StrutturaDatabaseForm(data).is_valid())
        
    def test_create_structure_invalid_data(self):
        data = {'nome': '', 'descrizione': ''}
        self.assertFalse(StrutturaDatabaseForm(data).is_valid())
    
