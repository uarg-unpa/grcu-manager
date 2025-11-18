"""Utilidades para la app accounts.

Funciones reutilizables relacionadas con usuarios, roles y redirecciones.
"""
from roles.models import Rol


def get_dashboard_for_user(user):
    """Devuelve el nombre de la ruta del dashboard según los roles del usuario.

    La prioridad es: Admin > Líder > Stakeholder > Visitante > Developer/otros.
    Retorna el nombre de la ruta tal como se usaría en `redirect(name)`.
    """
    if user.roles.filter(nombre=Rol.ADMIN).exists():
        return "dashboards:admin_dashboard"
    if user.roles.filter(nombre=Rol.LIDER).exists():
        return "dashboards:lider_dashboard"
    if user.roles.filter(nombre__iexact='Stakeholder').exists():
        return "dashboards:stakeholder_dashboard"
    if user.roles.filter(nombre__iexact='Visitante').exists():
        return "dashboards:visitor_dashboard"
    return "dashboards:developer_dashboard"
