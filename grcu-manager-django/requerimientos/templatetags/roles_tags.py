from django import template
from django.db.models import Q
from roles.models import Rol
from proyectos.models import ParticipacionProyecto

register = template.Library()

@register.filter
def es_stakeholder(user, proyecto):
    """
    Verifica si un usuario es stakeholder de un proyecto específico.
    Un usuario es stakeholder si:
    1. Tiene el rol 'Stakeholder' asignado
    2. Y está en la lista de clientes del proyecto
    """
    try:
        # Verificar que tenga el rol Stakeholder
        tiene_rol_stakeholder = user.roles.filter(nombre__iexact='Stakeholder').exists()
        
        # Verificar que esté en la lista de clientes del proyecto
        esta_en_clientes = proyecto.clientes.filter(id=user.id).exists()
        
        # Es stakeholder solo si cumple ambas condiciones
        return tiene_rol_stakeholder and esta_en_clientes
    except Exception:
        return False