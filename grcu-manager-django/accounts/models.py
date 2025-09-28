from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import Rol  # Importamos Rol desde la app roles

class Usuario(AbstractUser):
    avatar = models.URLField(blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)

    # Relación con roles (cada usuario puede tener varios roles)
    roles = models.ManyToManyField(Rol, related_name="usuarios")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.email})"

    # Chequear si el usuario es administrador
    def es_admin(self):
        return self.roles.filter(nombre__iexact="Admin").exists()


    # Chequear si el usuario tiene cierto permiso
    def tiene_permiso(self, permiso_nombre):
        # Se consulta a través de los roles relacionados
        return self.roles.filter(permisos__nombre__iexact=permiso_nombre).exists()
