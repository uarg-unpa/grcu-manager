from django.apps import AppConfig
from django.db.models.signals import post_migrate


def inicializar_fuentes_categorias(sender, **kwargs):
    """
    Inicializa fuentes y categorías predefinidas para todos los proyectos
    automáticamente después de las migraciones.
    """
    from proyectos.models import Proyecto
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
    
    # Categorías predefinidas (para requerimientos no funcionales)
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
    
    proyectos = Proyecto.objects.all()
    
    if proyectos.exists():
        fuentes_creadas = 0
        categorias_creadas = 0
        
        for proyecto in proyectos:
            # Crear fuentes predefinidas
            for fuente_nombre in FUENTES_PREDEFINIDAS:
                fuente, created = FuenteRequerimiento.objects.get_or_create(
                    proyecto=proyecto,
                    nombre=fuente_nombre,
                    defaults={
                        'es_predefinida': True,
                        'creado_por': proyecto.lider
                    }
                )
                if created:
                    fuentes_creadas += 1
            
            # Crear categorías predefinidas
            for categoria_nombre in CATEGORIAS_PREDEFINIDAS:
                categoria, created = CategoriaRequerimiento.objects.get_or_create(
                    proyecto=proyecto,
                    nombre=categoria_nombre,
                    defaults={
                        'es_predefinida': True,
                        'creado_por': proyecto.lider
                    }
                )
                if created:
                    categorias_creadas += 1
        
        if fuentes_creadas > 0 or categorias_creadas > 0:
            print(f"✅ Fuentes y categorías inicializadas: {fuentes_creadas} fuentes, {categorias_creadas} categorías")


class RequerimientosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requerimientos'
    
    def ready(self):
        # Importar signals para que se registren
        from . import signals
        
        # Inicializar fuentes y categorías después de migraciones
        post_migrate.connect(inicializar_fuentes_categorias, sender=self)
