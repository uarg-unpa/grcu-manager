"""
Configuración del panel de administración de Django para auditoría.

Este módulo configura la interfaz de administración para el modelo
RegistroActividad, estableciendo permisos de solo lectura para preservar
la integridad de los registros de auditoría.

Clases:
    RegistroActividadAdmin: Configuración del ModelAdmin para auditoría.
"""

from django.contrib import admin
from .models import RegistroActividad


@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para RegistroActividad.

    Proporciona una interfaz de solo lectura para consultar registros de
    auditoría. Los registros no pueden ser creados, editados o eliminados
    manualmente (excepto eliminación por superusuarios).

    Attributes:
        list_display (tuple): Campos mostrados en la lista.
        list_filter (tuple): Filtros disponibles en el sidebar.
        search_fields (tuple): Campos por los que se puede buscar.
        readonly_fields (tuple): Todos los campos son de solo lectura.
        date_hierarchy (str): Jerarquía de navegación por fecha.
    """

    list_display = (
        'usuario',
        'accion',
        'descripcion_corta',
        'ip_address',
        'fecha'
    )
    list_filter = ('accion', 'fecha')
    search_fields = ('usuario__email', 'usuario__nombre', 'descripcion')
    readonly_fields = (
        'usuario',
        'accion',
        'descripcion',
        'detalles',
        'ip_address',
        'user_agent',
        'fecha'
    )
    date_hierarchy = 'fecha'

    @admin.display(description='Descripción')
    def descripcion_corta(self, obj: RegistroActividad) -> str:
        """
        Muestra una versión truncada de la descripción.

        Args:
            obj (RegistroActividad): Instancia del registro.

        Returns:
            str: Descripción truncada a 50 caracteres si es necesario.
        """
        return (
            obj.descripcion[:50] + '...'
            if len(obj.descripcion) > 50
            else obj.descripcion
        )

    def has_add_permission(self, request) -> bool:
        """
        Desactiva la capacidad de crear registros manualmente.

        Args:
            request (HttpRequest): Request de Django.

        Returns:
            bool: Siempre False.
        """
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        Desactiva la capacidad de editar registros.

        Args:
            request (HttpRequest): Request de Django.
            obj (Optional[RegistroActividad]): Instancia del registro.

        Returns:
            bool: Siempre False.
        """
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """
        Permite eliminación solo a superusuarios.

        Args:
            request (HttpRequest): Request de Django.
            obj (Optional[RegistroActividad]): Instancia del registro.

        Returns:
            bool: True solo si el usuario es superusuario.
        """
        return request.user.is_superuser
