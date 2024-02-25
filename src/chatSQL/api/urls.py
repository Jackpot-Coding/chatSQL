from django.urls import path
from .views import *

urlpatterns = [
    path('', main),
    path('prompt/it', responseITA),
    path('prompt/en', responseENG),
]
