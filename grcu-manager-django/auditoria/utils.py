from .models import RegistroActividad


def get_client_ip(request):
    """Obtiene la IP del cliente desde el request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_actividad(request, accion, descripcion, detalles=None):
    """
    Registra una actividad del usuario en el sistema
    
    Args:
        request: HttpRequest object
        accion: Código de la acción (LOGIN, LOGOUT, etc.)
        descripcion: Descripción legible de la acción
        detalles: Dict con información adicional (opcional)
    
    Returns:
        RegistroActividad: El registro creado
    """
    return RegistroActividad.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        descripcion=descripcion,
        detalles=detalles or {},
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


def registrar_login(request):
    """Registra un inicio de sesión"""
    return registrar_actividad(
        request,
        'LOGIN',
        f"Usuario {request.user.email} inició sesión",
        {'email': request.user.email}
    )


def registrar_logout(request):
    """Registra un cierre de sesión"""
    return registrar_actividad(
        request,
        'LOGOUT',
        f"Usuario {request.user.email} cerró sesión",
        {'email': request.user.email}
    )


def registrar_creacion_usuario(request, usuario_creado):
    """Registra la creación de un usuario"""
    return registrar_actividad(
        request,
        'CREATE_USER',
        f"Se creó el usuario {usuario_creado.email}",
        {
            'usuario_creado_id': usuario_creado.id,
            'usuario_creado_email': usuario_creado.email,
            'roles': list(usuario_creado.roles.values_list('nombre', flat=True))
        }
    )


def registrar_eliminacion_usuario(request, usuario_eliminado):
    """Registra la eliminación de un usuario"""
    return registrar_actividad(
        request,
        'DELETE_USER',
        f"Se eliminó el usuario {usuario_eliminado.email}",
        {
            'usuario_eliminado_id': usuario_eliminado.id,
            'usuario_eliminado_email': usuario_eliminado.email,
        }
    )


def registrar_cambio_rol(request, usuario_modificado, roles_antiguos, roles_nuevos):
    """Registra un cambio de rol de usuario"""
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


def registrar_creacion_proyecto(request, proyecto):
    """Registra la creación de un proyecto"""
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


def registrar_eliminacion_proyecto(request, proyecto):
    """Registra la eliminación de un proyecto"""
    return registrar_actividad(
        request,
        'DELETE_PROJECT',
        f"Se eliminó el proyecto '{proyecto.nombre}'",
        {
            'proyecto_id': proyecto.id,
            'proyecto_nombre': proyecto.nombre
        }
    )


def registrar_creacion_grupo(request, grupo):
    """Registra la creación de un grupo"""
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


def registrar_eliminacion_grupo(request, grupo):
    """Registra la eliminación de un grupo"""
    return registrar_actividad(
        request,
        'DELETE_GROUP',
        f"Se eliminó el grupo '{grupo.nombre}'",
        {
            'grupo_id': grupo.id,
            'grupo_nombre': grupo.nombre
        }
    )
