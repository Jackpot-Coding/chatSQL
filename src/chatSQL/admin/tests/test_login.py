from django.test import TestCase,Client
from django.urls import reverse

from django.contrib.auth.models import User
from .. import forms

class LoginTestCase(TestCase):
   def setUp(self):
      User.objects.create_user(username="testAdmin",password="testPassword123!")

   def test_login_page_is_reachable(self):
      client = Client()
      response = client.get(reverse('admin_login'))
      self.assertEqual(response.status_code,200)

   def test_user_login_with_wrong_credentials(self):
      client = Client()
      response = client.post(reverse('admin_login'),{"username":"wronguser","password":"wrongpassword"})
      
      self.assertEqual(response.status_code,200)
      self.assertContains(response,"Credenziali non corrette")

   def test_user_login_with_right_credentials(self):
      client = Client()
      response = client.post(reverse('admin_login'),{"username":"testAdmin","password":"testPassword123!"})
      
      self.assertEqual(response.status_code,200)
      self.assertContains(response,"Autenticazione avvenuta con successo")


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


