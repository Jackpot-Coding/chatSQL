from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from ..forms import StrutturaDatabaseForm
from ..models import StrutturaDatabase

class adminTestCase(TestCase):
    
    client = Client
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
        self.client.login(username='testAdmin', password='testPassword123!')
    
    def test_admin_home_page_is_reachable(self):
        response = self.client.get(reverse("admin_home"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/home.html')
        
    def test_admin_home_page_has_no_structures(self):
        response = self.client.get(reverse("admin_home"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'Nessuna struttura database trovata.')
        
    def test_admin_home_page_displays_structures(self):
        
        db1 = StrutturaDatabase(nome="Test DB1",descrizione="Description for test1")
        db1.save()
        
        db2 = StrutturaDatabase(nome="Test DB2",descrizione="Description for test2")
        db2.save()
        
        response = self.client.get(reverse("admin_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'Test DB1')
        self.assertContains(response,"Test DB2")