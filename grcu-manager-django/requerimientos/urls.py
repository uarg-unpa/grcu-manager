from django.urls import path
from . import views

app_name = "requerimientos"

urlpatterns = [
    path('', views.requerimiento_list, name='requerimiento_list'),
    path('<int:pk>/', views.requerimiento_detail, name='requerimiento_detail'),
    path('create/', views.requerimiento_create, name='requerimiento_create'),
    path('create/<int:proyecto_id>/', views.requerimiento_create, name='requerimiento_create_proyecto'),
    path('priorizar/', views.requerimiento_priorizar, name='requerimiento_priorizar'),
]
