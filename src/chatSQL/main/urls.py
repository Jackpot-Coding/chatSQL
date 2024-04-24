from django.urls import path
from . import views

urlpatterns = [
   path('',views.MainView.as_view(),name='main'),
   path('getQuery',views.QueryGenerationView.as_view(),name="query_generation")
]