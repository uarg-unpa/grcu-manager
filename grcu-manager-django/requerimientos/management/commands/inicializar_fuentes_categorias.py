"""
Management command para inicializar fuentes y categorías predefinidas
en todos los proyectos existentes.
"""
from django.core.management.base import BaseCommand
from proyectos.models import Proyecto
from requerimientos.models import FuenteRequerimiento, CategoriaRequerimiento


class Command(BaseCommand):
    help = 'Inicializa fuentes y categorías predefinidas para todos los proyectos'

    def handle(self, *args, **options):
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
        total_proyectos = proyectos.count()
        
        self.stdout.write(f"Inicializando fuentes y categorías para {total_proyectos} proyecto(s)...")
        
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
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Inicialización completada:\n'
                f'   - {fuentes_creadas} fuentes creadas\n'
                f'   - {categorias_creadas} categorías creadas'
            )
        )
