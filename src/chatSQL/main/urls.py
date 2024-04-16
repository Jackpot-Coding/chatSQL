from django.urls import path
from . import views

urlpatterns = [
   path('natural_language/',views.NaturalLanguageView.as_view(),name='NaturalLanguageView'),
]