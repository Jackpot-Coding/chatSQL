from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from admin.models import StrutturaDatabase, Tabella, Campo

class NaturalLanguageTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
        StrutturaDatabase.objects.create(nome='db1', descrizione='Description')
        
        Tabella.objects.create(nome='clienti', descrizione='anagrafica clienti', struttura=StrutturaDatabase.objects.get(nome='db1'), sinonimi='clienti,cliente')
        Tabella.objects.create(nome='fatturato', descrizione='fatture effettuate', struttura=StrutturaDatabase.objects.get(nome='db1'), sinonimi='fattura,fatture,fatturato')
        
        Campo.objects.create(nome="id",tipo="INT",descrizione="indentificativo",sinonimi="identificativo",tabella=Tabella.objects.get(nome='clienti'))
        Campo.objects.create(nome="nome",tipo="VARCHAR",descrizione="Nome del cliente",sinonimi="nome,ragione sociale",tabella=Tabella.objects.get(nome='clienti'))
        Campo.objects.create(nome="indirizzo",tipo="VARCHAR",descrizione="Indirizzo sede",sinonimi="sede,locazione",tabella=Tabella.objects.get(nome='clienti'))
        
        Campo.objects.create(nome="id",tipo="INT",descrizione="indentificativo",sinonimi="identificativo",tabella=Tabella.objects.get(nome='fatturato'))
        Campo.objects.create(nome="data",tipo="DATE",descrizione="data di fatturazione",sinonimi="date,emissione",tabella=Tabella.objects.get(nome='fatturato'))
        Campo.objects.create(nome="euro",tipo="DOUBLE",descrizione="ammontare documento",sinonimi="totale,fatturato,prezzo",tabella=Tabella.objects.get(nome='fatturato'))

    def test_can_reach_natural_language_page(self):
        response = self.client.get(reverse('main'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_can_valid_input(self):
        data = {'natural_language': 'dammi clienti', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0) 
        
    def test_invalid_form(self):
        data = {'natural_language': '', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        
    def test_invalid_db_structure(self):
        data = {'natural_language': 'Natural Language', 'db_structure': ''}
        response = self.client.post(reverse('main'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    def test_not_inherent_natural_phrase(self):
        data = {'natural_language': 'give me an ice cream', 'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        
    def test_can_get_tabel_synonims(self):
        data = {'natural_language': 'dammi il nome dei clienti con sede a padova', 
                    'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response,'indirizzo di tipo VARCHAR contenente sede')
        
        
    def test_can_generate_prompt_with_two_tables(self):
        data = {'natural_language': 'dammi il nome dei clienti con fatturato totale maggiore di 2000 nel maggio 1990', 
                    'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response,'tabella clienti')
        self.assertContains(response,'tabella fatturato')
        
    def test_cannot_generate_tokens(self):
        data = {'natural_language': '`', 
                    'db_structure': StrutturaDatabase.objects.get(nome='db1').pk}
        response = self.client.post(reverse('main'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response,'Errore: impossibile interpretare la frase inserita.')
