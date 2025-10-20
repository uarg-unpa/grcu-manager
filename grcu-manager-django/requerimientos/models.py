from django.db import models
from proyectos.models import Proyecto
from accounts.models import Usuario
from typing import TYPE_CHECKING

# Type hints para Pylance
if TYPE_CHECKING:
    from typing import Optional


# Común a ambos tipos de gestión
class Requerimiento(models.Model):
    TIPO_CHOICES = [
        ("FUNCIONAL", "Funcional"),
        ("NO_FUNCIONAL", "No funcional"),
    ]
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("EN_PROGRESO", "En progreso"),
        ("COMPLETADO", "Completado"),
    ]
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="requerimientos")
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Adjuntos y recursos externos
    imagen = models.ImageField(upload_to='requerimientos/imagenes/', null=True, blank=True, 
                               help_text='Imagen adjunta (PNG, JPG, JPEG)')
    link_externo = models.URLField(max_length=500, blank=True, 
                                   help_text='Enlace a recurso externo')

    # Relaciones a detalles específicos
    detalle_tradicional = models.OneToOneField('DetalleRequerimientoTradicional', on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimiento', verbose_name="Detalle Tradicional")
    detalle_agil = models.OneToOneField('DetalleRequerimientoAgil', on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimiento', verbose_name="Detalle Ágil")

    # Relación opcional con Casos de Uso (muchos a muchos) usando tabla intermedia para mantener 3FN
    casos_relacionados = models.ManyToManyField('casos_de_uso.CasoDeUso', through='RequerimientoCaso', blank=True, related_name='requerimientos_relacionados')

    # Type hints para Pylance (campos OneToOne inversos y métodos dinámicos)
    if TYPE_CHECKING:
        detalle_tradicional_reverse: "Optional[DetalleRequerimientoTradicional]"
        detalle_agil_reverse: "Optional[DetalleRequerimientoAgil]"
        
        # Type hints para métodos dinámicos de Django (generados por choices)
        def get_tipo_display(self) -> str: ...
        def get_estado_display(self) -> str: ...

    def __str__(self):
        return self.nombre


# Detalles para gestión tradicional
class DetalleRequerimientoTradicional(models.Model):
    requerimiento_padre = models.OneToOneField(Requerimiento, on_delete=models.CASCADE, related_name='detalle_tradicional_reverse')

    prioridad = models.CharField(max_length=50, blank=True)
    fuente = models.CharField(max_length=255, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    fecha_compromiso = models.DateField(null=True, blank=True)
    estado_validacion = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Tradicional: {self.requerimiento_padre.nombre}"


# Detalles para gestión ágil
class DetalleRequerimientoAgil(models.Model):
    requerimiento_padre = models.OneToOneField(Requerimiento, on_delete=models.CASCADE, related_name='detalle_agil_reverse')

    historia_usuario = models.TextField(blank=True)
    criterio_aceptacion = models.TextField(blank=True)
    puntos_estimados = models.PositiveIntegerField(null=True, blank=True)
    sprint_asignado = models.CharField(max_length=100, blank=True)
    responsable = models.CharField(max_length=100, blank=True)
    estado_scrum = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Ágil: {self.requerimiento_padre.nombre}"


class RequerimientoCaso(models.Model):
    """Tabla intermedia que persiste la relación entre Requerimiento y CasoDeUso.
    Permite extender con atributos en el futuro sin violar 3FN."""
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='relaciones_casos')
    caso_de_uso = models.ForeignKey('casos_de_uso.CasoDeUso', on_delete=models.CASCADE, related_name='relaciones_requerimientos')
    fecha_vinculacion = models.DateTimeField(auto_now_add=True)
    nota = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('requerimiento', 'caso_de_uso')

    def __str__(self):
        # usar .pk para evitar advertencias del analizador estático (pylance)
        return f"Req {self.requerimiento.pk} <-> CU {self.caso_de_uso.pk}"
