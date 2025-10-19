from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from roles.models import Rol
    from grupos.models import Grupo
    from proyectos.models import Proyecto

class UsuarioManager(BaseUserManager['Usuario']):
    use_in_migrations = True

    def _create_user(self, email: str, nombre: str, password: Optional[str] = None, **extra_fields: Any) -> 'Usuario':
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, nombre: str, password: Optional[str] = None, **extra_fields: Any) -> 'Usuario':
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, nombre, password, **extra_fields)

    def create_superuser(self, email: str, nombre: str, password: Optional[str] = None, **extra_fields: Any) -> 'Usuario':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, nombre, password, **extra_fields)


class Usuario(AbstractUser):
    avatar = models.URLField(blank=True, null=True)
    username = None
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)

    # Relación con roles (cada usuario puede tener múltiples roles)
    roles = models.ManyToManyField('roles.Rol', blank=True, related_name='usuarios')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()  # type: ignore

    def __str__(self):
        return f"{self.nombre} ({self.email})"

    # Chequear si el usuario es administrador
    def es_admin(self):
        return self.roles.filter(nombre__iexact='Admin').exists()

    def es_lider(self):
        return self.roles.filter(nombre__iexact='Líder').exists()

    # Chequear si el usuario tiene cierto permiso
    def tiene_permiso(self, permiso_nombre):
        # Se consulta a través de los roles relacionados
        return self.roles.filter(permisos__nombre__iexact=permiso_nombre).exists()

    # Type hints para related managers (ayuda a Pylance)
    if TYPE_CHECKING:
        @property
        def lidera_proyectos(self) -> 'models.Manager[Proyecto]':
            """Proyectos donde este usuario es líder"""
            ...

        @property
        def proyectos(self) -> 'models.Manager[Proyecto]':
            """Proyectos donde este usuario es participante"""
            ...

        @property
        def lider_grupos(self) -> 'models.Manager[Grupo]':
            """Grupos donde este usuario es líder"""
            ...

        @property
        def grupos_creados(self) -> 'models.Manager[Grupo]':
            """Grupos creados por este usuario"""
            ...

        @property
        def grupos(self) -> 'models.Manager[Grupo]':
            """Grupos donde este usuario es integrante"""
            ...
