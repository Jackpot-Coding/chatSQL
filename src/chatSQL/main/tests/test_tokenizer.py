from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from admin.models import StrutturaDatabase

from main.prompt_creator import PromptCreator

class TransformersTestCase(TestCase):
    
    def setUp(self):
        self.mock_db = StrutturaDatabase()
        self.prompt_creator = PromptCreator(self.mock_db)

    def test_trova_sostantivi(self):
        # Testa diverse frasi di input con i sostantivi attesi
        casi_di_test = [
            ("Recupera i nomi di tutti i dipendenti.", ["nomi", "dipendenti"]),
            ("Prenota un volo per Parigi e i posti.", ["volo", "posti"]),
            ("Seleziona tutti i prodotti con un prezzo maggiore di 10.", ["prodotti", "prezzo"]),
            # Aggiungi altri casi di test se necessario
        ]

        for frase, sostantivi_attesi in casi_di_test:
            with self.subTest(frase=frase):
                sostantivi = self.prompt_creator.find_nouns(frase)[0]
                self.assertEqual(sostantivi, sostantivi_attesi)