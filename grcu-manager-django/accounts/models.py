"""
Modelos de usuarios personalizados para el sistema GRCU Manager.

Este módulo define el modelo de Usuario personalizado que extiende AbstractUser de Django,
utilizando email como identificador único en lugar de username. Incluye gestión de roles
y permisos a través de relaciones many-to-many.

Clases:
    UsuarioManager: Manager personalizado para creación de usuarios y superusuarios.
    Usuario: Modelo de usuario personalizado con autenticación por email.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from roles.models import Rol
    from grupos.models import Grupo
    from proyectos.models import Proyecto


class UsuarioManager(BaseUserManager['Usuario']):
    """
    Manager personalizado para el modelo Usuario.

    Proporciona métodos para crear usuarios regulares y superusuarios,
    utilizando email como campo de autenticación principal en lugar de username.

    Attributes:
        use_in_migrations (bool): Permite usar este manager en migraciones de datos.
    """

    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        nombre: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> 'Usuario':
        """
        Método privado para crear y guardar un usuario con email y contraseña.

        Args:
            email (str): Dirección de email del usuario (será normalizada).
            nombre (str): Nombre completo del usuario.
            password (Optional[str]): Contraseña en texto plano (será hasheada).
            **extra_fields: Campos adicionales del modelo Usuario.

        Returns:
            Usuario: Instancia del usuario creado y guardado en la base de datos.

        Raises:
            ValueError: Si el email no es proporcionado.
        """
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        nombre: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> 'Usuario':
        """
        Crea y guarda un usuario regular (no staff, no superusuario).

        Args:
            email (str): Dirección de email del usuario.
            nombre (str): Nombre completo del usuario.
            password (Optional[str]): Contraseña del usuario.
            **extra_fields: Campos adicionales del modelo Usuario.

        Returns:
            Usuario: Instancia del usuario creado.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, nombre, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        nombre: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> 'Usuario':
        """
        Crea y guarda un superusuario con permisos de staff y administrador.

        Args:
            email (str): Dirección de email del superusuario.
            nombre (str): Nombre completo del superusuario.
            password (Optional[str]): Contraseña del superusuario.
            **extra_fields: Campos adicionales del modelo Usuario.

        Returns:
            Usuario: Instancia del superusuario creado.

        Raises:
            ValueError: Si is_staff o is_superuser no están establecidos en True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, nombre, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado que utiliza email como identificador único.

    Extiende AbstractUser de Django, reemplazando el campo username por email
    como USERNAME_FIELD. Incluye gestión de roles mediante relación many-to-many
    y métodos de conveniencia para verificar permisos.

    Attributes:
        avatar (URLField): URL de la imagen de perfil del usuario (opcional).
        username (None): Campo deshabilitado (se usa email en su lugar).
        email (EmailField): Email único del usuario, usado para autenticación.
        nombre (CharField): Nombre completo del usuario.
        roles (ManyToManyField): Relación con el modelo Rol.

    Meta:
        USERNAME_FIELD: 'email' (campo usado para autenticación).
        REQUIRED_FIELDS: [] (sin campos adicionales requeridos).
    """

    avatar = models.URLField(blank=True, null=True)
    username = None
    email = models.EmailField(
        unique=True,
        db_index=True
    )  # Índice para búsquedas rápidas
    nombre = models.CharField(
        max_length=255,
        db_index=True
    )  # Índice para búsquedas rápidas

    # Relación con roles (cada usuario puede tener múltiples roles)
    roles = models.ManyToManyField(
        'roles.Rol',
        blank=True,
        related_name='usuarios'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()  # type: ignore

    def __str__(self) -> str:
        """
        Representación en string del usuario.

        Returns:
            str: Formato "Nombre (email@dominio.com)".
        """
        return f"{self.nombre} ({self.email})"

    def es_admin(self) -> bool:
        """
        Verifica si el usuario tiene el rol de Administrador.

        Returns:
            bool: True si el usuario es administrador, False en caso contrario.
        """
        return self.roles.filter(nombre__iexact='Admin').exists()

    def es_lider(self) -> bool:
        """
        Verifica si el usuario tiene el rol de Líder.

        Returns:
            bool: True si el usuario es líder, False en caso contrario.
        """
        return self.roles.filter(nombre__iexact='Líder').exists()

    def es_desarrollador(self) -> bool:
        """
        Verifica si el usuario tiene el rol de Desarrollador.

        Returns:
            bool: True si el usuario es desarrollador, False en caso contrario.
        """
        return self.roles.filter(nombre__iexact='Desarrollador').exists()

    def es_stakeholder(self) -> bool:
        """
        Verifica si el usuario tiene el rol de Stakeholder (cliente).

        Returns:
            bool: True si el usuario es stakeholder, False en caso contrario.
        """
        return self.roles.filter(nombre__iexact='Stakeholder').exists()

    def tiene_permiso(self, permiso_nombre: str) -> bool:
        """
        Verifica si el usuario tiene un permiso específico a través de sus roles.

        Args:
            permiso_nombre (str): Nombre del permiso a verificar.

        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario.
        """
        # Se consulta a través de los roles relacionados
        return self.roles.filter(
            permisos__nombre__iexact=permiso_nombre
        ).exists()

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
