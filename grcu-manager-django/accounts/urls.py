"""
Configuración de URLs para la aplicación accounts.

Define las rutas de autenticación del sistema, incluyendo login, logout,
setup del administrador inicial y callbacks de OAuth con Google.

Rutas:
    - setup-admin/: Configuración inicial del primer administrador
    - login/: Página de inicio de sesión
    - logout/: Cierre de sesión
    - google/login/: Inicio del flujo OAuth con Google
    - google/callback/: Callback de autenticación de Google
"""

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "setup-admin/",
        views.setup_admin,
        name="setup_admin"
    ),
    path(
        "login/",
        views.login_view,
        name="login"
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
    path(
        "google/login/",
        views.google_login_redirect,
        name="google_login_redirect"
    ),
    path(
        "google/callback/",
        views.google_login_callback,
        name="google_callback"
    ),
]
