from django.urls import path
from . import views

app_name = 'grupos'

urlpatterns = [
    path('', views.lista_grupos, name='lista_grupos'),
    path('nuevo/', views.crear_grupo, name='crear_grupo'),
    path('editar/<int:grupo_id>/', views.editar_grupo, name='editar_grupo'),
    path('eliminar/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    # API endpoints
    path('api/grupo/<int:grupo_id>/integrantes/', views.api_grupo_integrantes, name='api_grupo_integrantes'),
]
