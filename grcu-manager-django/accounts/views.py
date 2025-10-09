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

def setup_admin(request):
    # Si ya hay un admin, redirige al login
    if Usuario.objects.filter(roles__nombre__iexact="Admin").exists():
        messages.info(request, "Ya existe un administrador. Por favor, iniciá sesión.")
        return redirect("accounts:login")

    # Renderizar la plantilla de configuración del administrador
    return render(request, "accounts/setup_admin.html")


def login_view(request):
    # Verificar si hay usuarios en la base de datos
    # y si hay al menos un usuario con rol Admin
    if not Usuario.objects.exists() or not Usuario.objects.filter(roles__nombre__iexact="Admin").exists():
        return redirect("accounts:setup_admin")
    
    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


def google_login_redirect(request):
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
        messages.error(request, "No se pudo obtener el token de autenticación.")
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
    # try:
    #     idinfo = id_token.verify_oauth2_token(
    #         id_token_str, grequests.Request(), settings.GOOGLE_CLIENT_ID
    #     )
    # except ValueError as e:
    #     messages.error(request, f"Token inválido: {e}")
    #     return redirect("accounts:login")

    email = idinfo.get("email")
    full_name = idinfo.get("name", "")
    avatar_url = idinfo.get("picture", "")

    # Verificar si es el primer usuario (setup admin)
    if not Usuario.objects.filter(roles__nombre__iexact="Admin").exists():
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
            rol_admin, _ = Rol.objects.get_or_create(nombre="Admin")
            user.roles.add(rol_admin)
            user.save()
            messages.success(request, "Administrador configurado exitosamente.")
        login(request, user)
        return render(request, "accounts/setup_admin_success.html", {"email": email})

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

    if user.roles.filter(nombre__iexact="Admin").exists():
        return redirect("dashboards:admin_dashboard")
    elif user.roles.filter(nombre__iexact="Lider").exists():
        return redirect("dashboards:lider_dashboard")
    else:
        return redirect("dashboards:usuario_dashboard") 
    
    # return redirect("dashboards:admin_dashboard")