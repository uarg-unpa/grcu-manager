"""
Configuración de URLs para la aplicación auditoria.

Define las rutas del sistema de auditoría para administradores.
Actualmente todas las rutas redirigen a una página de "en desarrollo"
como placeholder para la demo.

Rutas:
    - admin/dashboard/: Dashboard principal de auditoría
    - admin/resumen/: Resumen de actividades recientes
    - admin/actividad/<id>/: Detalle de actividad específica
"""

from django.urls import path
from core import views as core_views

app_name = 'auditoria'

# Todas las rutas redirigen a "en desarrollo" para la demo
urlpatterns = [
    path(
        'admin/dashboard/',
        core_views.under_development,
        name='admin_dashboard'
    ),
    path(
        'admin/resumen/',
        core_views.under_development,
        name='auditoria_resumen'
    ),
    path(
        'admin/actividad/<int:actividad_id>/',
        core_views.under_development,
        name='actividad_detalle'
    ),
]
