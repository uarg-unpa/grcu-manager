from django.urls import path
from . import views

app_name = "requerimientos"

urlpatterns = [
    path('', views.requerimiento_list, name='requerimiento_list'),
    path('<int:pk>/', views.requerimiento_detail, name='requerimiento_detail'),
    path('create/', views.requerimiento_create, name='requerimiento_create'),
    path('create/<int:proyecto_id>/', views.requerimiento_create, name='requerimiento_create_proyecto'),
    path('<int:pk>/editar/', views.requerimiento_update, name='requerimiento_update'),
    path('<int:pk>/eliminar/', views.requerimiento_delete, name='requerimiento_delete'),
    path('priorizar/', views.requerimiento_priorizar, name='requerimiento_priorizar'),
    path('buscar/', views.buscar_requerimientos_ajax, name='buscar_requerimientos_ajax'),
    # Relacionar casos de uso existentes
    path('<int:pk>/relacionar-casos/', views.relacionar_casos_existentes, name='relacionar_casos_existentes'),
    # Historial
    path('<int:pk>/historial/', views.requerimiento_historial, name='requerimiento_historial'),
    path('<int:pk>/version/<int:version_id>/', views.requerimiento_version_detail, name='requerimiento_version_detail'),
    path('<int:pk>/comparar/<int:version_id1>/<int:version_id2>/', views.requerimiento_comparar_versiones, name='requerimiento_comparar_versiones'),
]
