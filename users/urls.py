from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("login/", edtech_login_view, name="edtech_login"),
    path("",home, name="edtech_home"),
    path("student/dashboard/", student_dashboard),
    path("teacher/dashboard/", teacher_dashboard),
    path("erp/dashboard/", admin_dashboard),
    path("logout/", logout_view, name="edtech_logout"),
    path("register/", edtech_register_view, name="edtech_register"),
    path('profile/', profile_view, name='edtech_profile'),
    path('edit/', edit_profile_view, name='edtech_edit_profile'),
    
]