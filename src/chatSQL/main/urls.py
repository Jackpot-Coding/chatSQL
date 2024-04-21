from django.urls import path
from . import views

urlpatterns = [
   path('',views.NaturalLanguageView.as_view(),name='NaturalLanguageView'),
]