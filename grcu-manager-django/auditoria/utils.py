"""
Utilidades para registro de actividades en el sistema de auditoría.

Este módulo proporciona funciones auxiliares para registrar diferentes tipos
de actividades en el sistema, facilitando el tracking de acciones importantes
como logins, cambios de roles, creación de recursos, etc.

Funciones:
    get_client_ip: Obtiene la IP del cliente desde el request.
    registrar_actividad: Función genérica para registrar cualquier actividad.
    registrar_login: Registra inicio de sesión.
    registrar_logout: Registra cierre de sesión.
    registrar_creacion_usuario: Registra creación de usuario.
    registrar_eliminacion_usuario: Registra eliminación de usuario.
    registrar_cambio_rol: Registra cambio de roles de usuario.
    registrar_creacion_proyecto: Registra creación de proyecto.
    registrar_eliminacion_proyecto: Registra eliminación de proyecto.
    registrar_creacion_grupo: Registra creación de grupo.
    registrar_eliminacion_grupo: Registra eliminación de grupo.
"""

from typing import Optional, Dict, Any
from django.http import HttpRequest
from .models import RegistroActividad


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Obtiene la dirección IP del cliente desde el request.

    Maneja correctamente requests detrás de proxies (como nginx)
    buscando primero en el header X-Forwarded-For.

    Args:
        request (HttpRequest): Objeto request de Django.

    Returns:
        Optional[str]: Dirección IP del cliente, o None si no se encuentra.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_actividad(
    request: HttpRequest,
    accion: str,
    descripcion: str,
    detalles: Optional[Dict[str, Any]] = None
) -> RegistroActividad:
    """
    Registra una actividad del usuario en el sistema.

    Función genérica que crea un registro de actividad con toda la
    información contextual necesaria (usuario, IP, user agent, etc).

    Args:
        request (HttpRequest): Objeto request de Django.
        accion (str): Código de la acción (LOGIN, LOGOUT, CREATE_USER, etc).
        descripcion (str): Descripción legible de la acción.
        detalles (Optional[Dict[str, Any]]): Diccionario con información
            adicional (opcional).

    Returns:
        RegistroActividad: El registro de actividad creado.
    """
    return RegistroActividad.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        descripcion=descripcion,
        detalles=detalles or {},
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


def registrar_login(request: HttpRequest) -> RegistroActividad:
    """
    Registra un inicio de sesión exitoso.

    Args:
        request (HttpRequest): Request con el usuario autenticado.

    Returns:
        RegistroActividad: Registro de la actividad de login.
    """
    return registrar_actividad(
        request,
        'LOGIN',
        f"Usuario {request.user.email} inició sesión",
        {'email': request.user.email}
    )


def registrar_logout(request: HttpRequest) -> RegistroActividad:
    """
    Registra un cierre de sesión.

    Args:
        request (HttpRequest): Request con el usuario autenticado.

    Returns:
        RegistroActividad: Registro de la actividad de logout.
    """
    return registrar_actividad(
        request,
        'LOGOUT',
        f"Usuario {request.user.email} cerró sesión",
        {'email': request.user.email}
    )


def registrar_creacion_usuario(
    request: HttpRequest,
    usuario_creado
) -> RegistroActividad:
    """
    Registra la creación de un nuevo usuario en el sistema.

    Args:
        request (HttpRequest): Request del admin que crea el usuario.
        usuario_creado (Usuario): Instancia del usuario creado.

    Returns:
        RegistroActividad: Registro de la actividad de creación.
    """
    return registrar_actividad(
        request,
        'CREATE_USER',
        f"Se creó el usuario {usuario_creado.email}",
        {
            'usuario_creado_id': usuario_creado.id,
            'usuario_creado_email': usuario_creado.email,
            'roles': list(
                usuario_creado.roles.values_list('nombre', flat=True)
            )
        }
    )


def registrar_eliminacion_usuario(
    request: HttpRequest,
    usuario_eliminado
) -> RegistroActividad:
    """
    Registra la eliminación de un usuario del sistema.

    Args:
        request (HttpRequest): Request del admin que elimina el usuario.
        usuario_eliminado (Usuario): Instancia del usuario eliminado.

    Returns:
        RegistroActividad: Registro de la actividad de eliminación.
    """
    return registrar_actividad(
        request,
        'DELETE_USER',
        f"Se eliminó el usuario {usuario_eliminado.email}",
        {
            'usuario_eliminado_id': usuario_eliminado.id,
            'usuario_eliminado_email': usuario_eliminado.email,
        }
    )


def registrar_cambio_rol(
    request: HttpRequest,
    usuario_modificado,
    roles_antiguos: list,
    roles_nuevos: list
) -> RegistroActividad:
    """
    Registra un cambio en los roles de un usuario.

    Args:
        request (HttpRequest): Request del admin que modifica los roles.
        usuario_modificado (Usuario): Usuario cuyos roles fueron modificados.
        roles_antiguos (list): Lista de nombres de roles anteriores.
        roles_nuevos (list): Lista de nombres de roles nuevos.

    Returns:
        RegistroActividad: Registro de la actividad de cambio de rol.
    """
    return registrar_actividad(
        request,
        'CHANGE_ROLE',
        f"Se modificaron los roles de {usuario_modificado.email}",
        {
            'usuario_id': usuario_modificado.id,
            'roles_antiguos': roles_antiguos,
            'roles_nuevos': roles_nuevos
        }
    )


def registrar_creacion_proyecto(
    request: HttpRequest,
    proyecto
) -> RegistroActividad:
    """
    Registra la creación de un nuevo proyecto.

    Args:
        request (HttpRequest): Request del usuario que crea el proyecto.
        proyecto (Proyecto): Instancia del proyecto creado.

    Returns:
        RegistroActividad: Registro de la actividad de creación.
    """
    return registrar_actividad(
        request,
        'CREATE_PROJECT',
        f"Se creó el proyecto '{proyecto.nombre}'",
        {
            'proyecto_id': proyecto.id,
            'proyecto_nombre': proyecto.nombre,
            'lider_id': proyecto.lider.id if proyecto.lider else None,
            'lider_email': proyecto.lider.email if proyecto.lider else None
        }
    )


def registrar_eliminacion_proyecto(
    request: HttpRequest,
    proyecto
) -> RegistroActividad:
    """
    Registra la eliminación de un proyecto.

    Args:
        request (HttpRequest): Request del usuario que elimina el proyecto.
        proyecto (Proyecto): Instancia del proyecto eliminado.

    Returns:
        RegistroActividad: Registro de la actividad de eliminación.
    """
    return registrar_actividad(
        request,
        'DELETE_PROJECT',
        f"Se eliminó el proyecto '{proyecto.nombre}'",
        {
            'proyecto_id': proyecto.id,
            'proyecto_nombre': proyecto.nombre
        }
    )


def registrar_creacion_grupo(
    request: HttpRequest,
    grupo
) -> RegistroActividad:
    """
    Registra la creación de un nuevo grupo.

    Args:
        request (HttpRequest): Request del usuario que crea el grupo.
        grupo (Grupo): Instancia del grupo creado.

    Returns:
        RegistroActividad: Registro de la actividad de creación.
    """
    return registrar_actividad(
        request,
        'CREATE_GROUP',
        f"Se creó el grupo '{grupo.nombre}'",
        {
            'grupo_id': grupo.id,
            'grupo_nombre': grupo.nombre,
            'integrantes_count': grupo.integrantes.count()
        }
    )


def registrar_eliminacion_grupo(
    request: HttpRequest,
    grupo
) -> RegistroActividad:
    """
    Registra la eliminación de un grupo.

    Args:
        request (HttpRequest): Request del usuario que elimina el grupo.
        grupo (Grupo): Instancia del grupo eliminado.

    Returns:
        RegistroActividad: Registro de la actividad de eliminación.
    """
    return registrar_actividad(
        request,
        'DELETE_GROUP',
        f"Se eliminó el grupo '{grupo.nombre}'",
        {
            'grupo_id': grupo.id,
            'grupo_nombre': grupo.nombre
        }
    )
