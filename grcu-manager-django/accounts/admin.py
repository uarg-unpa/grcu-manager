"""
Configuración del panel de administración de Django para el modelo Usuario.

Este módulo personaliza la interfaz de administración de Django para el modelo
Usuario personalizado, adaptando los campos mostrados, filtros y formularios
de creación/edición.

Clases:
    UsuarioAdmin: Configuración del ModelAdmin para el modelo Usuario.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del panel de administración para el modelo Usuario.

    Personaliza la interfaz de administración de Django para gestionar usuarios
    que utilizan email como identificador principal. Incluye configuración de
    campos mostrados en listas, filtros, búsqueda y formularios.

    Attributes:
        model (Model): Modelo Usuario al que aplica esta configuración.
        ordering (list): Orden de los registros en la lista (por email).
        list_display (list): Campos mostrados en la lista de usuarios.
        list_filter (list): Filtros disponibles en el sidebar.
        fieldsets (tuple): Organización de campos en el formulario de edición.
        add_fieldsets (tuple): Campos mostrados en el formulario de creación.
        search_fields (list): Campos por los que se puede buscar.
    """

    model = Usuario

    ordering = ['email']
    list_display = ['email', 'nombre']
    list_filter = ['roles']

    fieldsets = (
        (None, {
            'fields': ('email', 'nombre', 'password', 'roles')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'nombre',
                'password1',
                'password2',
                'roles',
                'is_staff',
                'is_active'
            )
        }),
    )

    search_fields = ['email', 'nombre']
