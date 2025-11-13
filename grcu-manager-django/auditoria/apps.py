"""
Configuración de la aplicación auditoria para Django.

Este módulo define la configuración básica de la aplicación auditoria,
responsable del registro y monitoreo de actividades del sistema.

Clases:
    AuditoriaConfig: Clase de configuración de la aplicación.
"""

from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    """
    Configuración de la aplicación auditoria.

    Define los parámetros básicos de configuración para la aplicación
    de auditoría y registro de actividades del sistema.

    Attributes:
        default_auto_field (str): Tipo de campo para auto-incremento de PKs.
        name (str): Nombre de la aplicación Django.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditoria'
