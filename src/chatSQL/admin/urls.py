from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('login/',views.AdminLoginView.as_view(),name="admin_login"),
   path('logout/',views.AdminLogoutView.as_view(),name="admin_logout"),
   path('',login_required(views.AdminHomeView.as_view(),login_url="/admin/login"),name="admin_home"),
   path('struttureDB/nuova',login_required(views.AdminStrutturaDatabaseView.as_view(),login_url="/admin/login"),name="new_db_view"),
   path('struttureDB/<int:structure_id>',login_required(views.AdminStrutturaDatabaseView.as_view(),login_url="/admin/login"),name="db_view"),
   path('elimina/<str:classe_modello>/<int:id_modello>',login_required(views.AdminEliminaModelView.as_view(),login_url='/admin/login'),name="model_delete"),
   path('tabella/', login_required(views.AdminCreaTabellaView.as_view(), login_url="/admin/login"), name="new_table_view"),
]