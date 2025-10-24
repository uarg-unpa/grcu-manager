from django.db import models
from accounts.models import Usuario


class RegistroActividad(models.Model):
    """
    Modelo para registrar actividades generales del sistema
    (login, logout, cambios administrativos, etc.)
    """
    ACCION_CHOICES = [
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('CREATE_USER', 'Creación de usuario'),
        ('UPDATE_USER', 'Modificación de usuario'),
        ('DELETE_USER', 'Eliminación de usuario'),
        ('CHANGE_ROLE', 'Cambio de rol'),
        ('CREATE_PROJECT', 'Creación de proyecto'),
        ('DELETE_PROJECT', 'Eliminación de proyecto'),
        ('CREATE_GROUP', 'Creación de grupo'),
        ('DELETE_GROUP', 'Eliminación de grupo'),
        ('ADMIN_ACTION', 'Acción administrativa'),
    ]
    
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='actividades'
    )
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    descripcion = models.TextField()
    detalles = models.JSONField(blank=True, null=True, help_text="Detalles adicionales en formato JSON")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Registro de Actividad'
        verbose_name_plural = 'Registros de Actividad'
        indexes = [
            models.Index(fields=['-fecha']),
            models.Index(fields=['usuario', '-fecha']),
            models.Index(fields=['accion']),
        ]
    
    def __str__(self):
        usuario_str = self.usuario.nombre if self.usuario else "Sistema"
        return f"{self.accion} - {usuario_str} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"

