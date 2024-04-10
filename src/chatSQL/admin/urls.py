from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
   path('login/',views.AdminLoginView.as_view(),name="admin_login")
]