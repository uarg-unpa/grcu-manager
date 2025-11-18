"""
Signals para la app de requerimientos.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from proyectos.models import Proyecto


@receiver(post_save, sender=Proyecto)
def crear_fuentes_categorias_nuevo_proyecto(sender, instance, created, **kwargs):
    """
    Cuando se crea un nuevo proyecto, automáticamente crea las fuentes
    y categorías predefinidas para ese proyecto.
    """
    if created:  # Solo cuando se crea un nuevo proyecto
        from .models import FuenteRequerimiento, CategoriaRequerimiento
        
        # Fuentes predefinidas
        FUENTES_PREDEFINIDAS = [
            'Entrevista con stakeholder/Cliente',
            'Documento de requerimientos',
            'Observación de usuario',
            'Encuesta / Cuestionario',
            'Análisis de sistema existente',
            'Solicitud del cliente',
        ]
        
        # Categorías predefinidas
        CATEGORIAS_PREDEFINIDAS = [
            'Seguridad',
            'Rendimiento',
            'Usabilidad',
            'Mantenibilidad',
            'Compatibilidad',
            'Disponibilidad',
            'Escalabilidad',
            'Confiabilidad',
        ]
        
        # Crear fuentes predefinidas para el nuevo proyecto
        for fuente_nombre in FUENTES_PREDEFINIDAS:
            FuenteRequerimiento.objects.create(
                proyecto=instance,
                nombre=fuente_nombre,
                es_predefinida=True,
                creado_por=instance.lider
            )
        
        # Crear categorías predefinidas para el nuevo proyecto
        for categoria_nombre in CATEGORIAS_PREDEFINIDAS:
            CategoriaRequerimiento.objects.create(
                proyecto=instance,
                nombre=categoria_nombre,
                es_predefinida=True,
                creado_por=instance.lider
            )
        
        print(f"✅ Fuentes y categorías creadas automáticamente para el proyecto '{instance.nombre}'")
