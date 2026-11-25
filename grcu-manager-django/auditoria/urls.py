"""
Configuración de URLs para la aplicación auditoria.

Define las rutas del sistema de auditoría para administradores.

Rutas:
    - admin/dashboard/: Dashboard principal de auditoría
    - admin/resumen/: Resumen de actividades recientes
    - admin/actividad/<id>/: Detalle de actividad específica
"""

from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path(
        'admin/dashboard/',
        views.admin_auditoria_dashboard,
        name='admin_dashboard'
    ),
    path(
        'admin/resumen/',
        views.auditoria_resumen,
        name='auditoria_resumen'
    ),
    path(
        'admin/actividad/<int:actividad_id>/',
        views.admin_auditoria_detalle,
        name='actividad_detalle'
    ),
]
