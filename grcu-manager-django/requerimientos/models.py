from django.db import models
from proyectos.models import Proyecto
from accounts.models import Usuario
from simple_history.models import HistoricalRecords
from typing import TYPE_CHECKING
from django.conf import settings

# Type hints para Pylance
if TYPE_CHECKING:
    from typing import Optional


# Común a ambos tipos de gestión
class Requerimiento(models.Model):
    TIPO_CHOICES = [
        ("FUNCIONAL", "Funcional"),
        ("NO_FUNCIONAL", "No funcional"),
        ("SISTEMA", "Sistema"),
    ]
    ESTADO_CHOICES = [
        ("BORRADOR", "Borrador"),
        ("VALIDADO", "Validado"),
        ("PRIORIZADO", "Priorizado"),
        ("EN_PROCESO", "En proceso"),
        ("TERMINADO", "Terminado"),
    ]
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="BORRADOR")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="requerimientos")
    
    # Campos para validación
    validado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimientos_validados')
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    TIPO_VALIDADOR_CHOICES = [
        ("CLIENTE", "Cliente/Stakeholder"),
        ("LIDER", "Líder de proyecto"),
    ]
    tipo_validador = models.CharField(max_length=20, choices=TIPO_VALIDADOR_CHOICES, null=True, blank=True)
    
    # Campos para manejo de rechazos y discusiones
    requiere_discusion = models.BooleanField(default=False, help_text='Indica si el requerimiento necesita discusión adicional')
    motivo_rechazo = models.TextField(blank=True, help_text='Motivo del último rechazo si aplica')
    ultimo_rechazado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='requerimientos_rechazados')
    fecha_ultimo_rechazo = models.DateTimeField(null=True, blank=True)
    
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Adjuntos y recursos externos
    imagen = models.ImageField(upload_to='requerimientos/imagenes/', null=True, blank=True, 
                               help_text='Imagen adjunta (PNG, JPG, JPEG)')
    link_externo = models.URLField(max_length=500, blank=True, 
                                   help_text='Enlace a recurso externo')

    # Relaciones a detalles específicos - se acceden desde los modelos de detalle como reverse relations

    # Relación opcional con Casos de Uso (muchos a muchos) usando tabla intermedia para mantener 3FN
    casos_relacionados = models.ManyToManyField('casos_de_uso.CasoDeUso', through='RequerimientoCaso', blank=True, related_name='requerimientos_relacionados')

    # Dependencias entre requerimientos (auto-referencial)
    dependencias = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependientes', help_text='Requerimientos de los que depende este requerimiento')

    # ⚡ HISTORIAL DE VERSIONES
    history = HistoricalRecords()

    # Type hints para Pylance (campos OneToOne inversos y métodos dinámicos)
    if TYPE_CHECKING:
        detalle_tradicional: "Optional[DetalleRequerimientoTradicional]"
        detalle_agil: "Optional[DetalleRequerimientoAgil]"
        
        # Type hints para métodos dinámicos de Django (generados por choices)
        def get_tipo_display(self) -> str: ...
        def get_estado_display(self) -> str: ...

    def __str__(self):
        return self.nombre


# Detalles para gestión tradicional
class DetalleRequerimientoTradicional(models.Model):
    requerimiento_padre = models.OneToOneField(Requerimiento, on_delete=models.CASCADE, related_name='detalle_tradicional')

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
    requerimiento_padre = models.OneToOneField(Requerimiento, on_delete=models.CASCADE, related_name='detalle_agil')

    prioridad = models.CharField(max_length=50, blank=True)
    historia_usuario = models.TextField(blank=True)
    criterio_aceptacion = models.TextField(blank=True)
    puntos_estimados = models.PositiveIntegerField(null=True, blank=True)
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


# ============================================================================
# MODELOS PARA VALIDACIÓN Y COMENTARIOS
# ============================================================================

class ComentarioValidacion(models.Model):
    """
    Modelo para comentarios y discusiones durante el proceso de validación de requerimientos.
    Permite hilos de conversación entre validadores, líderes y desarrolladores.
    Soporta diferentes tipos de comentarios según el contexto y participantes.
    """
    TIPO_ACCION_CHOICES = [
        ("VALIDAR", "Validar"),
        ("RECHAZAR", "Rechazar"),
        ("RESPUESTA", "Respuesta"),
        ("ACLARACION", "Aclaración"),
    ]
    
    TIPO_COMENTARIO_CHOICES = [
        ("DISCUSION_INTERNA", "Discusión Interna"),      # Líder + Desarrolladores
        ("VALIDACION_CLIENTE", "Validación con Cliente"), # Líder + Cliente (visible para devs)
        ("IMPLEMENTACION", "Implementación"),             # Post-validación
    ]

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='comentarios_validacion')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios_validacion')
    comentario = models.TextField(help_text='Comentario o explicación sobre la validación/rechazo')
    tipo_accion = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES, help_text='Tipo de acción que representa este comentario')
    tipo_comentario = models.CharField(
        max_length=20, 
        choices=TIPO_COMENTARIO_CHOICES, 
        default='DISCUSION_INTERNA',
        help_text='Contexto del comentario: interno del equipo, con cliente, o implementación'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Para respuestas/hilos de conversación
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas', help_text='Comentario padre si es una respuesta')
    
    # Metadata adicional
    es_respuesta = models.BooleanField(default=False, help_text='Indica si este comentario es una respuesta a otro')
    nivel_respuesta = models.PositiveIntegerField(default=0, help_text='Nivel de anidación en el hilo de conversación')
    
    # ⚡ HISTORIAL DE VERSIONES
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['fecha_creacion']
        verbose_name = 'Comentario de Validación'
        verbose_name_plural = 'Comentarios de Validación'
    
    def __str__(self):
        return f"{self.autor.nombre} - {self.get_tipo_accion_display()} - {self.requerimiento.nombre[:30]}"
    
    def save(self, *args, **kwargs):
        # Calcular si es respuesta y nivel
        if self.comentario_padre:
            self.es_respuesta = True
            self.nivel_respuesta = self.comentario_padre.nivel_respuesta + 1
        else:
            self.es_respuesta = False
            self.nivel_respuesta = 0
        super().save(*args, **kwargs)
    
    # Type hints para Pylance
    if TYPE_CHECKING:
        def get_tipo_accion_display(self) -> str: ...
