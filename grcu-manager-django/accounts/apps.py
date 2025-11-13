"""
Configuración de la aplicación accounts para Django.

Este módulo define la configuración básica de la aplicación accounts,
incluyendo el tipo de campo auto-generado para claves primarias.

Clases:
    AccountsConfig: Clase de configuración de la aplicación.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuración de la aplicación accounts.

    Define los parámetros básicos de configuración para la aplicación
    de cuentas de usuario y autenticación.

    Attributes:
        default_auto_field (str): Tipo de campo para auto-incremento de PKs.
        name (str): Nombre de la aplicación Django.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
