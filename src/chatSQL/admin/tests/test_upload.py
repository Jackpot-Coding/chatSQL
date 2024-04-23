from django.test import TestCase,Client
from django.urls import reverse

import os

from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from django.core.files.uploadedfile import SimpleUploadedFile

from ..views import AdminUploadFileView
from ..models import StrutturaDatabase, Tabella, Campo

class UploadFileTestCase(TestCase):
    
    client = Client()
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
            # Get the directory path of the test file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the file path relative to the test file
        file_path = os.path.join(test_dir, 'assets', 'db_test.json')
        # Open the file and create a SimpleUploadedFile object
        with open(file_path, 'rb') as file:
            file_data = file.read()
            self.file_obj = SimpleUploadedFile('db_test.json', file_data, content_type='application/json')
        # Construct the file path relative to the test file
        file_path = os.path.join(test_dir, 'assets', 'wrong_format.txt')
        # Open the file and create a SimpleUploadedFile object
        with open(file_path, 'rb') as file:
            file_data = file.read()
            self.wrong_file_obj = SimpleUploadedFile('wrong_format.txt', file_data, content_type='text/plain')

    def test_can_reach_upload_page(self):
        response = self.client.get(reverse('admin_upload_structure'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/upload_file.html')

    def test_upload_file(self):
        
        response = self.client.post(reverse('admin_upload_structure'), {'file': self.file_obj})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/home.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'File caricato con successo')
    
    def test_upload_file_no_file(self):
        response = self.client.post(reverse('admin_upload_structure'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/upload_file.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Il form non è valido.')

    def test_upload_file_wrong_format(self):
        response = self.client.post(reverse('admin_upload_structure'), {'file': self.wrong_file_obj})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/upload_file.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Errore durante l\'upload del file: Errore: formato file non supportato')

    def test_structure_upload(self):
        response = self.client.post(reverse('admin_upload_structure'), {'file': self.file_obj})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/home.html')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'File caricato con successo')

        db = StrutturaDatabase.objects.get(nome='Test DB')
        self.assertEqual(db.descrizione, 'Database di prova')
        t1 = Tabella.objects.get(struttura=db, nome='CUS')
        self.assertEqual(t1.descrizione, 'Tabella contenente i clienti dell\'azienda')
        self.assertEqual(t1.sinonimi, 'clienti,cliente,acquirente,acquirenti')
        c1 = Campo.objects.get(tabella=t1, nome='id')
        self.assertEqual(c1.tipo, 'INT')
        self.assertEqual(c1.sinonimi, 'identificatore')