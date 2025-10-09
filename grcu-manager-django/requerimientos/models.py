from django.db import models
from proyectos.models import Proyecto
from accounts.models import Usuario


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

    # Relaciones a detalles específicos
    detalle_tradicional = models.OneToOneField('DetalleRequerimientoTradicional', on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimiento', verbose_name="Detalle Tradicional")
    detalle_agil = models.OneToOneField('DetalleRequerimientoAgil', on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimiento', verbose_name="Detalle Ágil")

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
