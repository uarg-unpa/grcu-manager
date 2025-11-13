"""
Aplicación accounts - Gestión de usuarios y autenticación.

Esta aplicación maneja la autenticación mediante Google OAuth 2.0,
la gestión de usuarios con modelo personalizado, y el sistema de roles
y permisos del sistema GRCU Manager.

Módulos:
    - models: Definición del modelo Usuario personalizado con autenticación por email.
    - views: Vistas de login, logout, setup admin y callbacks OAuth.
    - admin: Configuración del panel de administración.
    - urls: Rutas de autenticación.
    - tests: Tests unitarios para Usuario y UsuarioManager.
"""
