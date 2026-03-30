from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('specialization/<int:id>/', views.specialization_detail, name='specialization_detail'),
    path('subject/<int:id>/', views.subject_detail, name='subject_detail'),
    path('unit/<int:id>/', views.unit_detail, name='unit_detail'),
    path('topic/<int:id>/', views.topic_detail_with_breadcrumb, name='topic_detail'),
    path('search/', views.search, name='search'),
]