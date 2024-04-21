from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from ..forms import CampoForm
from ..models import StrutturaDatabase,Campo

class CreateFieldTestCase(TestCase):

    client=Client()

    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')

    def test_can_reach_field_creation_page(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        response=self.client.get(reverse('new_campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo.html')

    def test_table_does_not_exist(self):
        response=self.client.get(reverse('new_campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/base.html')
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertTrue("La tabella selezionata non esiste." in messages[0].message)

    def test_can_create_field(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        data={'nome':'Test field','tipo':'INT','descrizione':'Description for test','sinonimi':'Synonyms for test'}
        response=self.client.post(reverse('new_campo_view',args=(1,)),data)
        self.assertEqual(response.status_code,302)
        self.assertTrue(Campo.objects.filter(nome='Test field').exists())

    def test_invalid_form_for_field_creation(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        data={'nome':'','tipo':'','descrizione':'','sinonimi':''}
        response=self.client.post(reverse('new_campo_view',args=(1,)),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo.html')

    def test_create_field_duplicate_name(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        t=db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        t.campo_set.create(nome='Existing field',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')
        data={'nome':'Existing field','tipo':'INT','descrizione':'Description for test','sinonimi':'Synonyms for test'}
        response=self.client.post(reverse('new_campo_view',args=(1,)),data)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Un campo con questo nome è già esistente.')

    def test_can_reach_field_edit_page(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        t=db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        t.campo_set.create(nome='Test field',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')
        response = self.client.get(reverse("campo_view",args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo.html')

    def test_field_does_not_exist(self):
        response=self.client.get(reverse('campo_view',args=(1,)))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/base.html')
        messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertTrue("Il campo selezionato non esiste." in messages[0].message)

    def test_cannot_edit_field_with_other_existing_name(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        t=db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        t.campo_set.create(nome='Test field1',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')
        t.campo_set.create(nome='Test field2',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')
        data={'nome':'Test field1','tipo':'INT','descrizione':'Description for test','sinonimi':'Synonyms for test'}
        response=self.client.post(reverse('campo_view',args=(2,)),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'admin/campo.html')
        self.assertContains(response,'Un campo con questo nome è già esistente.')

    def test_can_edit_field(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        t=db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        t.campo_set.create(nome='Test field',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')
        data={'nome':'Test field edited','tipo':'VARCHAR','descrizione':'Description for test edited','sinonimi':'Synonyms for test edited'}
        response=self.client.post(reverse('campo_view',args=(1,)),data)
        editedField=Campo.objects.get(pk=1)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Test field edited')
        self.assertContains(response,'VARCHAR')
        self.assertContains(response,'Description for test edited')
        self.assertContains(response,'Synonyms for test edited')
        self.assertEqual(editedField.nome,'Test field edited')
        self.assertEqual(editedField.tipo,'VARCHAR')
        self.assertEqual(editedField.descrizione,'Description for test edited')
        self.assertEqual(editedField.sinonimi,'Synonyms for test edited')
        self.assertTemplateUsed(response,'admin/campo.html')

class CampoFormTestCase(TestCase):

    def test_create_field_invalid_name(self):
        data = {'nome':'','tipo':'VARCHAR','descrizione':'Description for test','sinonimi':'Synonyms for test'}
        self.assertFalse(CampoForm(data).is_valid())
        
    def test_create_structure_invalid_description(self):
        data = {'nome':'Test field','tipo':'VARCHAR','descrizione':'','sinonimi':'Synonyms for test'}
        self.assertFalse(CampoForm(data).is_valid())
        
    def test_create_structure_invalid_type(self):
        data = {'nome':'Test field','tipo':'','descrizione':'Description for test','sinonimi':'Synonyms for test'}
        self.assertFalse(CampoForm(data).is_valid())
        
class CampoModelTestCase(TestCase):
    
    def test_can_get_str_of_campo(self):
        db = StrutturaDatabase(nome="Test DB",descrizione="Description for test")
        db.save()
        t=db.tabella_set.create(nome="Test table",descrizione="Description for test",sinonimi="Synonyms for test")
        t.campo_set.create(nome='Test field',tipo='INT',descrizione='Description for test',sinonimi='Synonyms for test')

        campo = Campo.objects.get(pk=1)
        self.assertEqual(campo.__str__(),"Test field")
        