import json
from django.shortcuts import render, redirect
from accounts.models import Usuario
from roles.models import Rol
from permisos.models import Permiso
from django.contrib.auth.decorators import login_required
from proyectos.models import Proyecto
from django.contrib.admin.models import LogEntry  
from django.db.models import Count

@login_required
def lider_casos(request):
    from django.urls import reverse
    return redirect(reverse('casos_de_uso:caso_de_uso_list'))

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
import json

from accounts.models import Usuario
from proyectos.models import Proyecto
from grupos.models import Grupo

@login_required
def admin_dashboard(request):
    # Métricas generales
    total_usuarios = Usuario.objects.count()
    total_proyectos = Proyecto.objects.count()
    proyectos_activos = Proyecto.objects.filter(activo=True).count()
    proyectos_inactivos = Proyecto.objects.filter(activo=False).count()
    total_grupos = Grupo.objects.count()
    grupos_activos = Grupo.objects.filter(activo=True).count()
    grupos_inactivos = Grupo.objects.filter(activo=False).count()

    # Roles esperados
    roles_labels = ["Admin", "Líder", "Desarrollador", "Visitante"]

    # Conteo de usuarios por rol
    usuarios_roles_qs = (
        Usuario.objects
        .values("roles__nombre")
        .annotate(count=Count("id"))
        .order_by()
    )
    usuarios_roles_map = {item["roles__nombre"]: item["count"] for item in usuarios_roles_qs if item["roles__nombre"]}
    usuarios_por_rol = [usuarios_roles_map.get(rol, 0) for rol in roles_labels]

    # Serializamos para los gráficos
    roles_labels_json = json.dumps(roles_labels)
    usuarios_por_rol_json = json.dumps(usuarios_por_rol)

    proyectos_estado_labels = ["Activos", "Inactivos"]
    proyectos_estado_values = [proyectos_activos, proyectos_inactivos]
    proyectos_estado_labels_json = json.dumps(proyectos_estado_labels)
    proyectos_estado_values_json = json.dumps(proyectos_estado_values)

    grupos_estado_labels = ["Activos", "Inactivos"]
    grupos_estado_values = [grupos_activos, grupos_inactivos]
    grupos_estado_labels_json = json.dumps(grupos_estado_labels)
    grupos_estado_values_json = json.dumps(grupos_estado_values)

    # Últimas acciones
    ultimas_acciones = LogEntry.objects.select_related("user").order_by("-action_time")[:10]

    # Contexto para el template
    context = {
        "total_usuarios": total_usuarios,
        "total_proyectos": total_proyectos,
        "total_grupos": total_grupos,
        "usuarios_roles_labels": roles_labels,
        "usuarios_roles_labels_json": roles_labels_json,
        "usuarios_roles_values_json": usuarios_por_rol_json,
        "proyectos_estado_labels": proyectos_estado_labels,
        "proyectos_estado_labels_json": proyectos_estado_labels_json,
        "proyectos_estado_values_json": proyectos_estado_values_json,
        "grupos_estado_labels": grupos_estado_labels,
        "grupos_estado_labels_json": grupos_estado_labels_json,
        "grupos_estado_values_json": grupos_estado_values_json,
        "ultimas_acciones": ultimas_acciones,
        "page_title": "Panel de Administración",
    }

    return render(request, "dashboards/admin_dashboard.html", context)


@login_required
def admin_proyecto_detail(request, project_id):
    """
    Redirige a la vista de detalle del proyecto en la app proyectos.
    Mantiene compatibilidad con URLs antiguas.
    """
    from django.shortcuts import redirect
    return redirect('proyectos:proyecto_detail_admin', proyecto_id=project_id)


@login_required
def lider_dashboard(request):
    from requerimientos.models import Requerimiento
    from casos_de_uso.models import CasoDeUso
    from usuarios.models import AccionUsuario

    proyectos = Proyecto.objects.filter(lider=request.user)
    dashboard_data = []

    for proyecto in proyectos:
        integrantes = list(proyecto.participantes.all())
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
        casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)

        # Acciones recientes de los integrantes del proyecto
        acciones = AccionUsuario.objects.filter(usuario__in=integrantes).order_by('-fecha')[:20]

        # Huérfanos definidos por ausencia de relación en la tabla intermedia RequerimientoCaso
        reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
        casos_huerfanos = casos_de_uso.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
        reqs_huerfanos_ids = list(reqs_huerfanos.values_list('pk', flat=True))
        casos_huerfanos_ids = list(casos_huerfanos.values_list('pk', flat=True))
        total_huerfanos = reqs_huerfanos.count() + casos_huerfanos.count()

        reqs_relacionados = requerimientos.count() - reqs_huerfanos.count()
        casos_relacionados = casos_de_uso.count() - casos_huerfanos.count()

        dashboard_data.append({
            "proyecto": proyecto,
            "integrantes": integrantes,
            "requerimientos": requerimientos,
            "casos_de_uso": casos_de_uso,
            "acciones": acciones,
            "reqs_huerfanos": reqs_huerfanos,
            "reqs_huerfanos_ids": reqs_huerfanos_ids,
            "casos_huerfanos": casos_huerfanos,
            "casos_huerfanos_ids": casos_huerfanos_ids,
            "total_huerfanos": total_huerfanos,
            "reqs_relacionados": reqs_relacionados,
            "casos_relacionados": casos_relacionados,
            "necesita_metodologia": proyecto.necesita_metodologia(),  # ⚡ NUEVO
            "puede_cambiar_metodologia": proyecto.puede_cambiar_metodologia(),  # ⚡ NUEVO
        })

    return render(request, "dashboards/lider_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": "Dashboard - Líder"
    })

# simulaciones

@login_required
def lider_matriz(request):
    """
    Redirige a la matriz de trazabilidad del primer proyecto del líder.
    La matriz ahora está en la app proyectos donde corresponde.
    """
    from django.contrib import messages
    
    proyectos = Proyecto.objects.filter(lider=request.user)
    
    proyecto_id = request.GET.get('proyecto')
    if proyecto_id:
        proyecto = proyectos.filter(id=proyecto_id).first()
    else:
        proyecto = proyectos.first()
    
    if not proyecto:
        messages.error(request, 'No tienes proyectos asignados como líder.')
        return redirect('dashboards:lider_dashboard')
    
    # Redirigir a la matriz del proyecto
    return redirect('proyectos:matriz_trazabilidad', proyecto_id=proyecto.pk)

@login_required
def lider_requerimientos(request):
    # Redirigir directamente a la lista de requerimientos
    # La vista de requerimientos se encargará de detectar si es líder y filtrar automáticamente
    return redirect('requerimientos:requerimiento_list')


@login_required
def lider_reportes(request):
    """
    Redirige a los reportes del primer proyecto del líder.
    Los reportes ahora están en la app proyectos donde corresponde.
    """
    from django.contrib import messages
    from proyectos.models import Proyecto
    
    proyectos = Proyecto.objects.filter(lider=request.user)
    
    proyecto_id = request.GET.get('proyecto')
    if proyecto_id:
        proyecto = proyectos.filter(id=proyecto_id).first()
    else:
        proyecto = proyectos.first()
    
    if not proyecto:
        messages.error(request, 'No tienes proyectos asignados como líder.')
        return redirect('dashboards:lider_dashboard')
    
    # Redirigir a los reportes del proyecto
    return redirect('proyectos:proyecto_reportes', proyecto_id=proyecto.pk)

@login_required
def lider_priorizar(request):
    from django.urls import reverse
    return redirect(reverse('requerimientos:requerimiento_priorizar'))


@login_required
def developer_dashboard(request):
    """
    Dashboard para desarrolladores.
    Muestra los proyectos donde el usuario participa (no necesariamente lidera).
    Reutiliza las funcionalidades existentes de requerimientos, casos de uso, matriz y reportes.
    """
    from requerimientos.models import Requerimiento
    from casos_de_uso.models import CasoDeUso
    from proyectos.models import ParticipacionProyecto
    
    # Obtener proyectos donde el usuario participa
    proyectos = Proyecto.objects.filter(participantes=request.user)
    dashboard_data = []
    
    for proyecto in proyectos:
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
        casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
        
        # Calcular huérfanos (igual que en el dashboard del líder)
        reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
        casos_huerfanos = casos_de_uso.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
        
        reqs_relacionados = requerimientos.count() - reqs_huerfanos.count()
        casos_relacionados = casos_de_uso.count() - casos_huerfanos.count()
        
        # Obtener el rol del usuario en este proyecto
        try:
            participacion = ParticipacionProyecto.objects.get(usuario=request.user, proyecto=proyecto)
            rol_usuario = participacion.rol.nombre
        except ParticipacionProyecto.DoesNotExist:
            rol_usuario = "Desarrollador"  # Por defecto
        
        # Verificar si es el líder del proyecto
        es_lider = (proyecto.lider == request.user)
        
        dashboard_data.append({
            "proyecto": proyecto,
            "requerimientos": requerimientos,
            "casos_de_uso": casos_de_uso,
            "reqs_huerfanos": reqs_huerfanos,
            "casos_huerfanos": casos_huerfanos,
            "reqs_relacionados": reqs_relacionados,
            "casos_relacionados": casos_relacionados,
            "necesita_metodologia": proyecto.necesita_metodologia(),
            "rol_usuario": rol_usuario,
            "es_lider": es_lider,
        })
    
    return render(request, "dashboards/developer_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": "Dashboard - Desarrollador"
    })

