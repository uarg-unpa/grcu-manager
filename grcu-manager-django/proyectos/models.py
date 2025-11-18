from django.db import models
from django.conf import settings
from roles.models import Rol
from grupos.models import Grupo
from simple_history.models import HistoricalRecords
from typing import TYPE_CHECKING

# Para type hints de Pylance
if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from requerimientos.models import Requerimiento

class Proyecto(models.Model):
    METODOLOGIAS = [
        ("TRADICIONAL", "Tradicional"),
        ("AGIL", "Ágil"),
    ]

    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    metodologia = models.CharField(max_length=20, choices=METODOLOGIAS, null=True, blank=True)  # Líder la asigna después
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

    # Clientes/Stakeholders asignados al proyecto (NO pertenecen al grupo de desarrollo)
    clientes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="proyectos_como_cliente",
        blank=True,
        limit_choices_to={'roles__nombre': 'Stakeholder'}
    )

    # Visitantes asignados al proyecto (tienen acceso de solo lectura)
    visitantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="proyectos_como_visitante",
        blank=True,
        limit_choices_to={'roles__nombre': 'Visitante'}
    )

    # Relación muchos a muchos con usuarios vía una tabla intermedia
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ParticipacionProyecto",
        related_name="proyectos"
    )
    
    # ⚡ HISTORIAL DE VERSIONES
    history = HistoricalRecords()
    
    # Type hint para la relación inversa con Requerimiento (ayuda a Pylance)
    if TYPE_CHECKING:
        requerimientos: "RelatedManager[Requerimiento]"
        # Django crea automáticamente get_<field>_display() para campos con choices
        def get_metodologia_display(self) -> str: ...

    def __str__(self):
        return self.nombre
    
    def puede_cambiar_metodologia(self):
        """
        Verifica si se puede cambiar la metodología del proyecto.
        Solo se puede cambiar si NO hay requerimientos NI casos de uso cargados.
        """
        from casos_de_uso.models import CasoDeUso
        tiene_requerimientos = self.requerimientos.exists()
        tiene_casos = CasoDeUso.objects.filter(proyecto=self).exists()
        return not (tiene_requerimientos or tiene_casos)
    
    def necesita_metodologia(self):
        """
        Verifica si el proyecto necesita que se le asigne una metodología.
        """
        return self.metodologia is None or self.metodologia == ''
    
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
