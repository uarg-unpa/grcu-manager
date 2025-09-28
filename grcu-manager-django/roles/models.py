from django.db import models
from permisos.models import Permiso

class Rol(models.Model):
    ADMIN = "Admin"
    LIDER = "Líder"
    DESARROLLADOR = "Desarrollador"
    STAKEHOLDER = "Stakeholder"
    VISITANTE = "Visitante"
    # ...

    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.ManyToManyField(Permiso, related_name="roles", blank=True)
    color = models.CharField(max_length=7, default="#444c8a")
    icono_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    
    @classmethod
    def get_admin_role(cls):
        return cls.objects.get_or_create(
            nombre="Admin",
            defaults={"nombre": "Admin"}
        )[0]