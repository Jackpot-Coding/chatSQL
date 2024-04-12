from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import DatabaseStructureForm
from ..models import DatabaseStructure

class createStructureTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testuser', password='testpassword')

    def test_get_request(self):
        response = self.client.get(reverse('db_creation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/db_creation.html')

    def test_create_structure_success(self):
        data = {'name': 'Test Database', 'description': 'Test Description'}
        response = self.client.post(reverse('db_creation'), data)
        self.assertEqual(response.status_code, 200)  # Assuming you are rendering the form again after successful creation
        self.assertTrue(DatabaseStructure.objects.filter(name='Test Database').exists())
        
    def test_create_structure_duplicate_name(self):
        existing_structure = DatabaseStructure.objects.create(name='Existing Database', description='Existing Description')
        data = {'name': 'Existing Database', 'description': 'Test Description'}
        response = self.client.post(reverse('db_creation'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Un database con questo nome è già esistente.')
        self.assertFalse(DatabaseStructure.objects.filter(name='Test Database').exists())

class DatabaseStructureFormTestCase(TestCase):

    def test_create_structure_invalid_name(self):
        data = {'name': '', 'description': 'Test Description'}
        self.assertFalse(DatabaseStructureForm(data).is_valid())
        
    def test_create_structure_invalid_description(self):
        data = {'name': 'Test Database', 'description': ''}
        self.assertFalse(DatabaseStructureForm(data).is_valid())
        
    def test_create_structure_invalid_data(self):
        data = {'name': '', 'description': ''}
        self.assertFalse(DatabaseStructureForm(data).is_valid())
    
