from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from admin.models import StrutturaDatabase, Tabella

class fillNaturalLanguageTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        StrutturaDatabase.objects.create(nome='db1', descrizione='Description')
        Tabella.objects.create(nome='tab', descrizione='Description', struttura=StrutturaDatabase.objects.get(nome='db1'), sinonimi='sinonimo1,sinonimo2')
        pass

    def test_can_reach_natural_language_page(self):
        response = self.client.get(reverse('NaturalLanguageView'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'natural_language.html')

    def test_can_valid_input(self):
        data = {'natural_language': 'dammi tab', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('NaturalLanguageView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'natural_language.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0) 
        
    def test_invalid_form(self):
        data = {'natural_language': '', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('NaturalLanguageView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'natural_language.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        
    def test_invalid_db_structure(self):
        data = {'natural_language': 'Natural Language', 'db_structure': ''}
        response = self.client.post(reverse('NaturalLanguageView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'natural_language.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    def test_not_inherent_natural_phrase(self):
        data = {'natural_language': 'give me crauti', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('NaturalLanguageView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'natural_language.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)