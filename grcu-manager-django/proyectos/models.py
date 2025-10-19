from django.db import models
from django.conf import settings
from roles.models import Rol
from grupos.models import Grupo

class Proyecto(models.Model):
    METODOLOGIAS = [
        ("TRADICIONAL", "Tradicional"),
        ("AGIL", "Ágil"),
    ]

    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    metodologia = models.CharField(max_length=20, choices=METODOLOGIAS, default="AGIL")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="proyectos/logos/", blank=True, null=True)

    # Grupo asignado al proyecto (opcional)
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        related_name="proyectos",
        null=True,
        blank=True
    )

    # Clave foránea: el líder se elige entre los usuarios participantes
    lider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="lidera_proyectos",
        null=True,
        blank=True
    )

    # Relación muchos a muchos con usuarios vía una tabla intermedia
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ParticipacionProyecto",
        related_name="proyectos"
    )

    def __str__(self):
        return self.nombre
    
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proyectos_creados"
    )


class ParticipacionProyecto(models.Model):
    """
    Tabla intermedia para relacionar un Usuario con un Proyecto y un Rol dentro de ese proyecto.
    Resuelve el caso de 'cada usuario tiene un único rol por proyecto'.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "proyecto")  # Un usuario solo puede tener un rol en un proyecto

    def __str__(self):
        return f"{self.usuario.email} - {self.rol.nombre} en {self.proyecto.nombre}"
