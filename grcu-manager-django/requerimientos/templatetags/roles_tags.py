from django import template
from django.db.models import Q
from roles.models import Rol
from proyectos.models import ParticipacionProyecto

register = template.Library()

@register.filter
def es_stakeholder(user, proyecto):
    """
    Verifica si un usuario es stakeholder de un proyecto específico.
    """
    try:
        stakeholder_rol = Rol.objects.get(nombre='Stakeholder')
        return ParticipacionProyecto.objects.filter(
            usuario=user,
            proyecto=proyecto,
            rol=stakeholder_rol
        ).exists()
    except Rol.DoesNotExist:
        return False