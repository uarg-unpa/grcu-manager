"""
Vistas del sistema de auditoría para administradores.

Este módulo proporciona vistas para el dashboard de auditoría, permitiendo
a los administradores visualizar, filtrar y analizar todas las actividades
del sistema. Incluye métricas, gráficos y vistas detalladas de actividades.

Funciones:
    is_admin: Verifica si un usuario es administrador.
    admin_auditoria_dashboard: Dashboard principal de auditoría.
    auditoria_resumen: Resumen de actividades recientes.
    admin_auditoria_detalle: Vista detallada de una actividad específica.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, F
from django.utils import timezone
from datetime import timedelta
import json

from .models import RegistroActividad
from accounts.models import Usuario
from grupos.models import Grupo
from proyectos.models import Proyecto


def is_admin(user) -> bool:
    """
    Verifica si el usuario es administrador.

    Args:
        user (Usuario): Instancia del usuario a verificar.

    Returns:
        bool: True si el usuario es admin, False en caso contrario.
    """
    return (
        user.is_authenticated and
        user.roles.filter(nombre__iexact="Admin").exists()
    )


@login_required
@user_passes_test(is_admin)
def admin_auditoria_dashboard(request):
    """
    Dashboard de auditoría para administradores.

    Proporciona una vista completa del sistema de auditoría con:
    - Métricas generales (total de actividades, actividades 24h, etc.)
    - Filtros por acción, usuario, fecha, grupo y proyecto
    - Búsqueda por texto en descripción y usuarios
    - Gráficos de actividad por día
    - Rankings de usuarios, grupos y proyectos más activos
    - Paginación de resultados

    Args:
        request (HttpRequest): Request de Django con parámetros GET opcionales:
            - accion: Filtrar por tipo de acción
            - usuario: Filtrar por ID de usuario
            - fecha_desde: Filtrar desde fecha
            - fecha_hasta: Filtrar hasta fecha
            - grupo: Filtrar por ID de grupo
            - proyecto: Filtrar por ID de proyecto
            - q: Búsqueda de texto
            - page: Número de página para paginación

    Returns:
        HttpResponse: Renderiza auditoria_dashboard.html con contexto completo.
    """

    # === PARÁMETROS DE FILTRO ===
    filtro_accion = request.GET.get('accion', '')
    filtro_usuario = request.GET.get('usuario', '')
    filtro_fecha_desde = request.GET.get('fecha_desde', '')
    filtro_fecha_hasta = request.GET.get('fecha_hasta', '')
    filtro_grupo = request.GET.get('grupo', '')
    filtro_proyecto = request.GET.get('proyecto', '')
    busqueda = request.GET.get('q', '')

    # === CONSULTA BASE CON RELACIONES ===
    actividades = RegistroActividad.objects.select_related(
        'usuario'
    ).prefetch_related(
        'usuario__grupos',
        'usuario__roles',
        'usuario__lidera_proyectos',
        'usuario__proyectos'
    ).order_by('-fecha')

    # === APLICAR FILTROS ===
    if filtro_accion:
        actividades = actividades.filter(accion=filtro_accion)

    if filtro_usuario:
        actividades = actividades.filter(usuario__id=filtro_usuario)

    if filtro_fecha_desde:
        actividades = actividades.filter(fecha__date__gte=filtro_fecha_desde)

    if filtro_fecha_hasta:
        actividades = actividades.filter(fecha__date__lte=filtro_fecha_hasta)

    if busqueda:
        actividades = actividades.filter(
            Q(descripcion__icontains=busqueda) |
            Q(usuario__email__icontains=busqueda) |
            Q(usuario__nombre__icontains=busqueda)
        )

    if filtro_grupo:
        actividades = actividades.filter(usuario__grupos__id=filtro_grupo)

    if filtro_proyecto:
        # Filtrar por proyectos donde el usuario es líder O participante
        actividades = actividades.filter(
            Q(usuario__lidera_proyectos__id=filtro_proyecto) |
            Q(usuario__proyectos__id=filtro_proyecto)
        )

    # === MÉTRICAS GENERALES ===
    total_actividades = RegistroActividad.objects.count()
    actividades_filtradas = actividades.count()

    # Últimas 24 horas
    hace_24h = timezone.now() - timedelta(hours=24)
    actividades_24h = RegistroActividad.objects.filter(fecha__gte=hace_24h).count()

    # Actividades por tipo (últimos 30 días)
    hace_30d = timezone.now() - timedelta(days=30)
    actividades_por_tipo = (
        RegistroActividad.objects
        .filter(fecha__gte=hace_30d)
        .values('accion')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Usuarios más activos (últimos 30 días)
    usuarios_mas_activos = (
        RegistroActividad.objects
        .filter(fecha__gte=hace_30d)
        .values('usuario__email', 'usuario__nombre')
        .annotate(count=Count('id'))
        .exclude(usuario__isnull=True)
        .order_by('-count')[:10]
    )

        # Grupos más activos (últimos 30 días)
    fecha_limite_grupos = timezone.now() - timedelta(days=30)
    grupos_mas_activos = RegistroActividad.objects.filter(
        fecha__gte=fecha_limite_grupos,
        usuario__isnull=False
    ).values(
        'usuario__grupos__nombre'
    ).annotate(
        grupo__nombre=F('usuario__grupos__nombre'),
        count=Count('id')
    ).filter(
        grupo__nombre__isnull=False
    ).order_by('-count')[:5]

    # Calcular porcentajes para grupos
    if grupos_mas_activos:
        max_grupo_count = grupos_mas_activos[0]['count']
        for grupo in grupos_mas_activos:
            grupo['porcentaje'] = (grupo['count'] / max_grupo_count) * 100 if max_grupo_count > 0 else 0

    # Proyectos más activos (últimos 30 días)
    proyectos_mas_activos = RegistroActividad.objects.filter(
        fecha__gte=fecha_limite_grupos,
        usuario__isnull=False
    ).values(
        'usuario__proyectos__nombre'
    ).annotate(
        proyecto__nombre=F('usuario__proyectos__nombre'),
        count=Count('id')
    ).filter(
        proyecto__nombre__isnull=False
    ).order_by('-count')[:5]

    # Calcular porcentajes para proyectos
    if proyectos_mas_activos:
        max_proyecto_count = proyectos_mas_activos[0]['count']
        for proyecto in proyectos_mas_activos:
            proyecto['porcentaje'] = (proyecto['count'] / max_proyecto_count) * 100 if max_proyecto_count > 0 else 0

    # === DATOS PARA GRÁFICOS ===
    # Actividades por día (últimos 7 días)
    hace_7d = timezone.now() - timedelta(days=7)
    actividades_por_dia = (
        RegistroActividad.objects
        .filter(fecha__gte=hace_7d)
        .extra(select={'dia': "DATE(fecha)"})
        .values('dia')
        .annotate(count=Count('id'))
        .order_by('dia')
    )

    # Preparar datos para Chart.js
    dias_labels = []
    dias_values = []
    for i in range(7):
        dia = (timezone.now() - timedelta(days=6-i)).date()
        dias_labels.append(dia.strftime('%d/%m'))
        count = next((item['count'] for item in actividades_por_dia if item['dia'] == str(dia)), 0)
        dias_values.append(count)

    # Datos del gráfico para JavaScript
    chart_data = {
        'labels': dias_labels,
        'data': dias_values
    }

    # === PAGINACIÓN ===
    from django.core.paginator import Paginator
    paginator = Paginator(actividades, 25)  # 25 actividades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # === DATOS PARA FILTROS ===
    acciones_disponibles = RegistroActividad.ACCION_CHOICES
    usuarios_disponibles = Usuario.objects.filter(is_active=True).order_by('email')
    grupos_disponibles = Grupo.objects.filter(activo=True).order_by('nombre')
    proyectos_disponibles = Proyecto.objects.filter(activo=True).order_by('nombre')

    # === CONTEXTO ===
    context = {
        'page_title': 'Auditoría del Sistema',
        'total_actividades': total_actividades,
        'actividades_filtradas': actividades_filtradas,
        'actividades_24h': actividades_24h,
        'actividades_por_tipo': actividades_por_tipo,
        'usuarios_mas_activos': usuarios_mas_activos,
        'grupos_mas_activos': grupos_mas_activos,
        'proyectos_mas_activos': proyectos_mas_activos,
        'page_obj': page_obj,
        'actividades': page_obj,  # Alias para compatibilidad

        # Datos para gráficos
        'auditoria_chart_data': chart_data,

        # Datos para filtros
        'acciones_disponibles': acciones_disponibles,
        'usuarios_disponibles': usuarios_disponibles,
        'grupos_disponibles': grupos_disponibles,
        'proyectos_disponibles': proyectos_disponibles,

        # Valores de filtros actuales
        'filtro_accion': filtro_accion,
        'filtro_usuario': filtro_usuario,
        'filtro_fecha_desde': filtro_fecha_desde,
        'filtro_fecha_hasta': filtro_fecha_hasta,
        'filtro_grupo': filtro_grupo,
        'filtro_proyecto': filtro_proyecto,
        'busqueda': busqueda,
    }

    return render(request, 'auditoria/auditoria_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def auditoria_resumen(request):
    """
    Vista que devuelve las últimas 10 actividades para dashboards.

    Proporciona un resumen ligero de actividades recientes que puede ser
    incluido en otros dashboards del sistema. Optimizada para carga rápida
    con select_related.

    Args:
        request (HttpRequest): Request de Django.

    Returns:
        HttpResponse: Renderiza auditoria_resumen.html con actividades recientes.
    """
    actividades_recientes = (
        RegistroActividad.objects
        .select_related('usuario')
        .order_by('-fecha')[:10]
    )

    context = {
        'actividades_recientes': actividades_recientes,
    }

    return render(request, 'auditoria/auditoria_resumen.html', context)


@login_required
@user_passes_test(is_admin)
def admin_auditoria_detalle(request, actividad_id):
    """
    Vista detallada de una actividad específica.

    Muestra toda la información disponible de una actividad particular,
    incluyendo detalles JSON, metadatos (IP, user agent), y actividades
    relacionadas del mismo usuario.

    Args:
        request (HttpRequest): Request de Django.
        actividad_id (int): ID del registro de actividad a mostrar.

    Returns:
        HttpResponse: Renderiza auditoria_detalle.html con información completa.

    Raises:
        Http404: Si no existe una actividad con el ID especificado.
    """
    actividad = get_object_or_404(RegistroActividad, id=actividad_id)

    # Obtener actividades relacionadas del mismo usuario (últimas 10)
    actividades_relacionadas = []
    if actividad.usuario:
        actividades_relacionadas = (
            RegistroActividad.objects
            .filter(usuario=actividad.usuario)
            .exclude(id=actividad.pk)
            .order_by('-fecha')[:10]
        )

    context = {
        'page_title': f'Actividad #{actividad.pk}',
        'actividad': actividad,
        'actividades_relacionadas': actividades_relacionadas,
    }

    return render(request, 'auditoria/auditoria_detalle.html', context)
