from django.urls import path
from . import views

urlpatterns = [
   path('prompt/',views.PromptView.as_view(),name='prompt')
]