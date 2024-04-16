from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import TabellaForm
from ..models import Tabella
from ..models import StrutturaDatabase

class CreateTableTestCase(TestCase):
    client = Client()

    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        
    def test_can_reach_table_creation_page(self):
        response = self.client.get(reverse('new_table_view'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/tabella.html')
        
    def test_can_create_table(self):
        data_db = {'nome': 'Test Tab Str', 'descrizione': 'Test Db Descrizione'}
        self.client.post(reverse('new_db_view'), data_db)
        
        db_id = StrutturaDatabase.objects.filter(nome=data_db.get('nome')).first()
        
        data = {'nome': 'Test Table', 
                'descrizione': 'Test Table Description', 
                'sinonimi': 'Test Sinonimi', 
                'struttura': db_id.pk
            }
        response = self.client.post(reverse('new_table_view'), data)
        self.assertEqual(response.status_code, 200) #tabella creata
        self.assertTrue(Tabella.objects.filter(nome='Test Table').exists())