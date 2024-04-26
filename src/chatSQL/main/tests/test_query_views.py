from django.test import TestCase,Client
from django.urls import reverse

from ..query_generator import QueryGenerator

from unittest.mock import patch

class QueryGenerationViewsTestCase(TestCase):
    
    client = Client
    
    def setUp(self):
        pass
    
    def test_empty_prompt_error(self):
        response = self.client.post(reverse("query_generation"),data={"prompt":''})

        self.assertTemplateUsed(response,'main.html')
        self.assertContains(response,"Prompt non fornito")
    

    def test_can_get_query(self):
        
        with patch.object(QueryGenerator, 'get_query',return_value="```SELECT * FROM Clienti WHERE nome LIKE '%SRL%'```"):
            response = self.client.post(reverse("query_generation"),data={"prompt":'dammi i clienti'})
        
            self.assertTemplateUsed(response,'query.html')
            self.assertContains(response,'<code>')
        
    def test_cannot_interpret_prompt(self):
        with patch.object(QueryGenerator, 'get_query',return_value="interpretation"):
            response = self.client.post(reverse("query_generation"),data={"prompt":'dammi i clienti'})
        
            self.assertTemplateUsed(response,'main.html')
            self.assertContains(response,'Errore di interpretazione del prompt')
        
    def test_cannot_contact_api_service(self):
        with patch.object(QueryGenerator, 'get_query',return_value="error"):
            response = self.client.post(reverse("query_generation"),data={"prompt":'dammi i clienti'})
        
            self.assertTemplateUsed(response,'main.html')
            self.assertContains(response,'Errore di comunicazione con servizio di generazione query.')