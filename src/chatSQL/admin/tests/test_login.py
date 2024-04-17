from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from .. import forms

class LoginTestCase(TestCase):

    client = Client()

    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")

    def test_login_page_is_reachable(self):
        response = self.client.get(reverse('admin_login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'admin/login.html')
        
    def test_user_login_with_wrong_credentials(self):
        response = self.client.post(reverse('admin_login'),{"username":"wronguser","password":"wrongpassword"})
    
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Credenziali non corrette")

    def test_user_login_with_right_credentials(self):
        response = self.client.post(reverse('admin_login'),{"username":"testAdmin","password":"testPassword123!"})
    
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Autenticazione avvenuta con successo")  
        
    def test_user_login_with_no_credentials(self):
        response = self.client.post(reverse('admin_login'),{"username":"","password":""})
    
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'admin/login.html')


class LogoutTestCase(TestCase):
    
    client = Client()
    
    def setUp(self):
        User.objects.create_user(username="testAdmin",password="testPassword123!")
    
    def test_can_logout_if_authenticated(self):
        self.client.post(reverse('admin_login'),{"username":"testAdmin","password":"testPassword123!"})
        response = self.client.get(reverse('admin_logout'))
        
        self.assertEqual(response.wsgi_request.user.is_authenticated,False)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('admin_login'))
    
    def test_cannot_logout_if_not_authenticated(self):
        response = self.client.get(reverse('admin_logout'))
        
        messages = [msg for msg in get_messages(response.wsgi_request)]
        
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('admin_login'))
        self.assertEqual(messages[0].tags,"error")
        self.assertTrue("Impossibile effettuare il logout" in messages[0].message)


class LoginFormTestCase(TestCase):

    def test_login_form_username_field_label(self):
        form = forms.LoginForm()
        self.assertEqual(form.fields["username"].label,"Nome Utente")

    def test_login_form_password_field_label(self):
        form = forms.LoginForm()
        self.assertEqual(form.fields["password"].label,"Password")

    def test_login_form_invalid_without_username(self):
        form = forms.LoginForm(data={"username":"","password":"wrongPassword123"})
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_without_password(self):
        form = forms.LoginForm(data={"username":"wrongUsername","password":""})
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_without_data(self):
        form = forms.LoginForm(data={"username":"","password":""})
        self.assertFalse(form.is_valid())


