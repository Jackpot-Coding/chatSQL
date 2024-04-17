from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import CampoTabella
from ..models import Campo

class CreateFieldTestCase(TestCase):

    client=Client()

    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')

    def test_can_reach_field_creation_page(self):
        response=self.client.get(reverse('new_campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo_tabella.html')

    """def test_can_create_structure(self):
        data={'nome':'Test Campo','tipo':'INT','descrizione':'Test descrizione',}"""