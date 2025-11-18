"""
Vistas de autenticación y gestión de usuarios para GRCU Manager.

Este módulo maneja la autenticación mediante Google OAuth 2.0, el setup inicial
del administrador del sistema, y las operaciones de login/logout. Incluye validación
de dominios permitidos y registro de auditoría.

Funciones:
    setup_admin: Configura el primer usuario administrador del sistema.
    login_view: Renderiza la página de login.
    logout_view: Cierra la sesión del usuario actual.
    google_login_redirect: Redirige al flujo de autenticación de Google.
    google_login_callback: Procesa el callback de Google OAuth.
"""

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from urllib.parse import urlencode
from django.conf import settings
from .models import Usuario
import requests
from django.contrib import messages
from roles.models import Rol
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from auditoria.utils import registrar_login, registrar_logout


def setup_admin(request):
    """
    Vista para configurar el primer administrador del sistema.

    Si ya existe un administrador, redirige al login. Esta vista solo está
    disponible durante el setup inicial del sistema.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.

    Returns:
        HttpResponse: Renderiza setup_admin.html o redirige a login.
    """
    # Si ya hay un admin, redirige al login
    if Usuario.objects.filter(roles__nombre=Rol.ADMIN).exists():
        messages.info(
            request,
            "Ya existe un administrador. Por favor, iniciá sesión."
        )
        return redirect("accounts:login")

    # Renderizar la plantilla de configuración del administrador
    return render(
        request,
        "accounts/setup_admin.html",
        {"page_title": "Configurar Administrador"}
    )


def login_view(request):
    """
    Vista principal de inicio de sesión.

    Verifica si existe al menos un administrador en el sistema. Si no existe,
    redirige al setup inicial. Si existe, muestra la página de login con
    autenticación de Google.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.

    Returns:
        HttpResponse: Renderiza login.html o redirige a setup_admin.
    """
    # Verificar si hay usuarios en la base de datos
    # y si hay al menos un usuario con rol Admin
    if not Usuario.objects.exists() or \
       not Usuario.objects.filter(roles__nombre=Rol.ADMIN).exists():
        return redirect("accounts:setup_admin")

    return render(
        request,
        "accounts/login.html",
        {"page_title": "Bienvenido a GRCU Manager"}
    )


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión del usuario actual.

    Registra el logout en el sistema de auditoría antes de cerrar la sesión
    y redirige al login.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.

    Returns:
        HttpResponseRedirect: Redirige a la página de login.
    """
    # Registrar logout antes de cerrar sesión
    registrar_logout(request)
    logout(request)
    return redirect("accounts:login")


def google_login_redirect(request):
    """
    Inicia el flujo de autenticación OAuth 2.0 con Google.

    Construye la URL de autorización de Google con los parámetros necesarios
    y redirige al usuario para que autorice la aplicación.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.

    Returns:
        HttpResponseRedirect: Redirige a la página de autorización de Google.
    """
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": request.build_absolute_uri("/accounts/google/callback/"),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    return redirect(f"{url}?{urlencode(params)}")


def google_login_callback(request):
    """
    Procesa el callback de autenticación de Google OAuth 2.0.

    Intercambia el código de autorización por tokens de acceso, verifica
    el ID token, valida el dominio del email, y crea o actualiza el usuario.
    También maneja el caso especial del primer administrador del sistema.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP con el código de autorización.

    Returns:
        HttpResponse: Redirige al dashboard correspondiente según el rol del usuario,
                     renderiza página de éxito en setup, o redirige a login en caso de error.

    Flujo:
        1. Obtiene el código de autorización de los parámetros GET.
        2. Intercambia el código por tokens con Google.
        3. Verifica y decodifica el ID token.
        4. Valida que el email pertenezca a un dominio permitido.
        5. Crea el primer admin si no existe, o busca usuario existente.
        6. Actualiza información del usuario (nombre, avatar).
        7. Inicia sesión y redirige según el rol.
    """
    code = request.GET.get("code")
    if not code:
        messages.error(request, "Error en la autenticación con Google.")
        return redirect("accounts:login")

    # Solicitud del token
    token_url = "https://oauth2.googleapis.com/token"
    redirect_uri = request.build_absolute_uri("/accounts/google/callback/")
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    token_resp = requests.post(token_url, data=data).json()
    id_token_str = token_resp.get("id_token")
    if not id_token_str:
        messages.error(
            request,
            "No se pudo obtener el token de autenticación."
        )
        return redirect("accounts:login")

    # Verificación del id_token
    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str, grequests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        # Mostrar el mensaje original del error
        messages.error(request, f"Token inválido: {e}")
        print("Error de validación del token:", e)
        return redirect("accounts:login")

    email = idinfo.get("email")
    full_name = idinfo.get("name", "")
    avatar_url = idinfo.get("picture", "")

    # Validar dominio permitido
    allowed_domains = ["gmail.com", "uarg.unpa.edu.ar"]
    if not any(email.endswith(f"@{domain}") for domain in allowed_domains):
        messages.error(
            request,
            "Solo se permiten emails de los dominios: "
            "@gmail.com o @uarg.unpa.edu.ar"
        )
        return redirect("accounts:login")

    # Verificar si es el primer usuario (setup admin)
    if not Usuario.objects.filter(roles__nombre=Rol.ADMIN).exists():
        # Crear el usuario como administrador
        user, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                "nombre": full_name,
                "avatar": avatar_url,
                "is_active": True,
            }
        )
        if created:
            # Asignar rol de administrador
            rol_admin, _ = Rol.objects.get_or_create(nombre=Rol.ADMIN)
            user.roles.add(rol_admin)
            user.save()
            messages.success(
                request,
                "Administrador configurado exitosamente."
            )
        login(request, user)
        return render(
            request,
            "accounts/setup_admin_success.html",
            {"email": email}
        )

    # Si ya hay un admin, buscar usuario existente
    user = Usuario.objects.filter(email=email).first()
    if not user:
        messages.error(request, "No estás registrado en el sistema.")
        return redirect("accounts:login")

    # Actualizar datos del usuario
    user.nombre = full_name
    if avatar_url:
        user.avatar = avatar_url
    user.save(update_fields=["nombre", "avatar"])

    # Loguear usuario
    login(request, user)

    # Registrar login en auditoría
    registrar_login(request)

    # Redirigir según rol (verificar en orden de prioridad)
    if user.roles.filter(nombre=Rol.ADMIN).exists():
        return redirect("dashboards:admin_dashboard")
    elif user.roles.filter(nombre=Rol.LIDER).exists():
        return redirect("dashboards:lider_dashboard")
    elif user.roles.filter(nombre__iexact='Stakeholder').exists():
        # Stakeholders/Clientes van a su dashboard específico
        return redirect("dashboards:stakeholder_dashboard")
    elif user.roles.filter(nombre__iexact='Visitante').exists():
        # Visitantes van a su dashboard específico
        return redirect("dashboards:visitor_dashboard")
    else:
        # Desarrolladores y otros roles
        return redirect("dashboards:developer_dashboard")
