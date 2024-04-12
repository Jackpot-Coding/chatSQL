from django.urls import path
from . import views

urlpatterns = [
   path('login/',views.AdminLoginView.as_view(),name="admin_login"),
   path('db_creation/',views.CreateStructureView.as_view(),name="db_creation"),
   path('db_list/',views.DatabaseListView.as_view(),name="db_list"),
]