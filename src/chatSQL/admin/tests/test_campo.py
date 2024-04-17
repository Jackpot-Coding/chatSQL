from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from ..forms import CampoForm
from ..models import StrutturaDatabase,Tabella,Campo

class CreateFieldTestCase(TestCase):

    client=Client()

    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')

    def test_can_reach_field_creation_page(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="synonyms for test")
        response=self.client.get(reverse('new_campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo.html')

    def test_table_does_not_exist(self):
        response=self.client.get(reverse('new_campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/base.html')
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertTrue("La tabella selezionata non esiste." in messages[0].message)

    """def test_can_create_structure(self):
        data={'nome':'Test Campo','tipo':'INT','descrizione':'Test descrizione',}"""