from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('login/',views.AdminLoginView.as_view(),name="admin_login"),
   path('',login_required(views.AdminHomeView.as_view(),login_url="/admin/login"),name="admin_home"),
   path('struttureDB/nuova',login_required(views.AdminStrutturaDatabaseView.as_view(),login_url="/admin/login"),name="new_db_view"),
   path('struttureDB/<int:id>',login_required(views.AdminStrutturaDatabaseView.as_view(),login_url="/admin/login"),name="db_view")
]