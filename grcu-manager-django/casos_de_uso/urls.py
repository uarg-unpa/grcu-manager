from django.urls import path
from . import views

app_name = "casos_de_uso"

urlpatterns = [
    path('', views.caso_de_uso_list, name='caso_de_uso_list'),
    path('proyecto/<int:proyecto_id>/', views.caso_de_uso_list, name='caso_de_uso_list'),
    path('crear/<int:proyecto_id>/', views.caso_de_uso_create, name='caso_de_uso_create'),
    path('<int:pk>/', views.caso_de_uso_detail, name='caso_de_uso_detail'),
    path('<int:pk>/editar/', views.caso_de_uso_update, name='caso_de_uso_update'),
    path('<int:pk>/eliminar/', views.caso_de_uso_delete, name='caso_de_uso_delete'),
    path('buscar/', views.buscar_casos_de_uso_ajax, name='buscar_casos_de_uso_ajax'),
    
    # URLs de historial
    path('<int:pk>/historial/', views.caso_de_uso_historial, name='caso_de_uso_historial'),
    path('<int:pk>/historial/<int:history_id>/', views.caso_de_uso_version_detail, name='caso_de_uso_version_detail'),
    path('<int:pk>/comparar/', views.caso_de_uso_comparar_versiones, name='caso_de_uso_comparar_versiones'),
]
