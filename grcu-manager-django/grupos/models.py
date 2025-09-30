from django.db import models
from accounts.models import Usuario

class Grupo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="grupos/logos/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="grupos_creados")
    activo = models.BooleanField(default=True)
    integrantes = models.ManyToManyField(Usuario, related_name="grupos")

    def __str__(self):
        return self.nombre
