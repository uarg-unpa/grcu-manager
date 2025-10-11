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
    from proyectos.models import Proyecto
    from requerimientos.models import Requerimiento
    from casos_de_uso.models import CasoDeUso
    from usuarios.models import AccionUsuario

    proyecto = Proyecto.objects.filter(id=project_id).first()
    if not proyecto:
        return render(request, 'dashboards/admin_project_detail.html', {'error': 'Proyecto no encontrado'})

    integrantes = list(proyecto.participantes.all())
    lider = proyecto.lider
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    casos = CasoDeUso.objects.filter(proyecto=proyecto)
    acciones = AccionUsuario.objects.filter(usuario__in=integrantes).order_by('-fecha')[:20]

    # Huérfanos definidos como aquellos sin relación persistida en la tabla intermedia RequerimientoCaso
    from requerimientos.models import RequerimientoCaso
    reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
    casos_huerfanos = casos.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
    reqs_huerfanos_ids = list(reqs_huerfanos.values_list('pk', flat=True))
    casos_huerfanos_ids = list(casos_huerfanos.values_list('pk', flat=True))

    # Matriz de trazabilidad simple: relacionar requerimientos y casos por nombre parcial (heurística)
    matriz = []
    for req in requerimientos:
        relacionados = [cu for cu in casos if req.nombre.split()[0].lower() in cu.nombre.lower() or req.nombre.lower() in cu.descripcion.lower()]
        matriz.append({'req': req, 'casos': relacionados})

    # Agregaciones para gráficos
    # Requerimientos por estado
    req_estado_qs = requerimientos.values('estado').annotate(count=Count('id'))
    req_estado_map = {item['estado']: item['count'] for item in req_estado_qs}
    req_estado_labels = ["PENDIENTE", "EN_PROGRESO", "COMPLETADO"]
    req_estado_values = [req_estado_map.get(k, 0) for k in req_estado_labels]

    # Requerimientos por tipo
    req_tipo_qs = requerimientos.values('tipo').annotate(count=Count('id'))
    req_tipo_map = {item['tipo']: item['count'] for item in req_tipo_qs}
    req_tipo_labels = ["FUNCIONAL", "NO_FUNCIONAL"]
    req_tipo_values = [req_tipo_map.get(k, 0) for k in req_tipo_labels]

    # Casos de uso: conteo por disponibilidad de detalle (Tradicional / Ágil / Sin detalle)
    casos_trad = casos.filter(detalle_tradicional__isnull=False).count()
    casos_agil = casos.filter(detalle_agil__isnull=False).count()
    casos_sin = casos.filter(detalle_agil__isnull=True, detalle_tradicional__isnull=True).count()
    casos_tipo_labels = ["Tradicional", "Ágil", "Sin detalle"]
    casos_tipo_values = [casos_trad, casos_agil, casos_sin]

    # Acciones por usuario (top 5)
    acciones_por_usuario_qs = AccionUsuario.objects.filter(usuario__in=integrantes).values('usuario__nombre').annotate(count=Count('id')).order_by('-count')[:5]
    acciones_labels = [a['usuario__nombre'] for a in acciones_por_usuario_qs]
    acciones_values = [a['count'] for a in acciones_por_usuario_qs]

    return render(request, 'dashboards/admin_project_detail.html', {
        'proyecto': proyecto,
        'integrantes': integrantes,
        'lider': lider,
        'requerimientos': requerimientos,
        'casos': casos,
        'acciones': acciones,
        'reqs_huerfanos': reqs_huerfanos,
    'reqs_huerfanos_ids': reqs_huerfanos_ids,
        'casos_huerfanos': casos_huerfanos,
    'casos_huerfanos_ids': casos_huerfanos_ids,
        'matriz': matriz,
        # Datos para gráficos
        'req_estado_labels': req_estado_labels,
        'req_estado_values': req_estado_values,
        'req_tipo_labels': req_tipo_labels,
        'req_tipo_values': req_tipo_values,
        'casos_tipo_labels': casos_tipo_labels,
        'casos_tipo_values': casos_tipo_values,
        'acciones_labels': acciones_labels,
        'acciones_values': acciones_values,
    })

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
        })

    return render(request, "dashboards/lider_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": "Dashboard - Líder"
    })

# simulaciones

@login_required
def lider_matriz(request):
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_matriz.html')

@login_required
def lider_requerimientos(request):
    # Redirigir directamente a la lista de requerimientos
    # La vista de requerimientos se encargará de detectar si es líder y filtrar automáticamente
    return redirect('requerimientos:requerimiento_list')


@login_required
def lider_reportes(request):
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_reportes.html')

@login_required
def lider_priorizar(request):
    from django.urls import reverse
    return redirect(reverse('requerimientos:requerimiento_priorizar'))
