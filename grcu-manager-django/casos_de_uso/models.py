from django.db import models
from proyectos.models import Proyecto
from accounts.models import Usuario
from simple_history.models import HistoricalRecords

class CasoDeUso(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="casos_de_uso")
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Adjuntos y recursos externos
    imagen = models.ImageField(upload_to='casos_de_uso/imagenes/', null=True, blank=True,
                               help_text='Imagen adjunta (PNG, JPG, JPEG)')
    link_externo = models.URLField(max_length=500, blank=True,
                                   help_text='Enlace a recurso externo')

    # Relaciones a detalles específicos
    detalle_tradicional = models.OneToOneField('DetalleCasoDeUsoTradicional', on_delete=models.SET_NULL, null=True, blank=True, related_name='caso_de_uso', verbose_name="Detalle Tradicional")
    detalle_agil = models.OneToOneField('DetalleCasoDeUsoAgil', on_delete=models.SET_NULL, null=True, blank=True, related_name='caso_de_uso', verbose_name="Detalle Ágil")

    # HISTORIAL DE VERSIONES
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

class DetalleCasoDeUsoTradicional(models.Model):
    caso_de_uso_padre = models.OneToOneField(CasoDeUso, on_delete=models.CASCADE, related_name='detalle_tradicional_reverse')
    actor_principal = models.CharField(max_length=255, blank=True)
    precondiciones = models.TextField(blank=True)
    flujo_principal = models.TextField(blank=True)
    flujo_alternativo = models.TextField(blank=True)
    postcondiciones = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Tradicional: {self.caso_de_uso_padre.nombre}"

class DetalleCasoDeUsoAgil(models.Model):
    caso_de_uso_padre = models.OneToOneField(CasoDeUso, on_delete=models.CASCADE, related_name='detalle_agil_reverse')
    historia_usuario = models.TextField(blank=True)
    criterio_aceptacion = models.TextField(blank=True)
    responsable = models.CharField(max_length=100, blank=True)
    estado_scrum = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Ágil: {self.caso_de_uso_padre.nombre}"
