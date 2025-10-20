from django.urls import path
from . import views

app_name = "casos_de_uso"

urlpatterns = [
    path('', views.caso_de_uso_list, name='caso_de_uso_list'),
    path('proyecto/<int:proyecto_id>/', views.caso_de_uso_list, name='caso_de_uso_list'),
    path('crear/<int:proyecto_id>/', views.caso_de_uso_create, name='caso_de_uso_create'),
    path('<int:pk>/', views.caso_de_uso_detail, name='caso_de_uso_detail'),
    path('buscar/', views.buscar_casos_de_uso_ajax, name='buscar_casos_de_uso_ajax'),
]
