from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from admin.models import StrutturaDatabase

from ..views import PromptView

class fillNaturalLanguageTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        StrutturaDatabase.objects.create(nome='db1', descrizione='Description')
        pass

    def test_can_reach_natural_language_page(self):
        response = self.client.get(reverse('PromptView'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prompt.html')

    '''    
    Per il momento non utilizzabile poiché non c'è la strutture delle tabelle
    quindi, poiché la view chiama il metodo per la costruzione del prompt,
    che va in errore non trovando la struttura delle tabelle, manderà sempre 
    un messaggio di errore.
    
    def test_can_fill_natural_language(self):
        data = {'natural_language': 'Natural Language', 'db_structure': 'db1'}
        response = self.client.post(reverse('PromptView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prompt.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0) 
        
    '''
        
    def test_invalid_form_for_natural_language(self):
        data = {'natural_language': '', 'db_structure': 'db1'}
        response = self.client.post(reverse('PromptView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prompt.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        
    def test_invalid_db_structure_for_natural_language(self):
        data = {'natural_language': 'Natural Language', 'db_structure': ''}
        response = self.client.post(reverse('PromptView'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prompt.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)