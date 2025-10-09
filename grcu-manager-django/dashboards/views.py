from django.shortcuts import render, redirect
from accounts.models import Usuario
from roles.models import Rol
from permisos.models import Permiso
from django.contrib.auth.decorators import login_required
from proyectos.models import Proyecto
from django.contrib.admin.models import LogEntry  
from django.db.models import Count

@login_required
def admin_dashboard(request):
    total_usuarios = Usuario.objects.count()
    total_proyectos = Proyecto.objects.count()
    total_roles = Rol.objects.count()
    from grupos.models import Grupo
    total_grupos = Grupo.objects.count()

    ultimas_acciones = LogEntry.objects.select_related("user").order_by("-action_time")[:10]

    return render(request, "dashboards/admin_dashboard.html", {
        "total_usuarios": total_usuarios,
        "total_proyectos": total_proyectos,
        "total_roles": total_roles,
        "total_grupos": total_grupos,
        "ultimas_acciones": ultimas_acciones,
        "page_title": "Panel de Administración"
    })

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

    reqs_huerfanos = requerimientos.filter(detalle_agil__responsable="") | requerimientos.filter(detalle_agil__isnull=True, detalle_tradicional__isnull=True)
    casos_huerfanos = casos.filter(detalle_agil__responsable="") | casos.filter(detalle_agil__isnull=True, detalle_tradicional__isnull=True)

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
        'casos_huerfanos': casos_huerfanos,
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

        # Requerimientos huérfanos: sin responsable/asignación
        reqs_huerfanos = requerimientos.filter(
            detalle_agil__responsable="", detalle_tradicional__fuente=""
        ) | requerimientos.filter(
            detalle_agil__isnull=True, detalle_tradicional__isnull=True
        )

        # Casos de uso huérfanos: sin responsable/asignación
        casos_huerfanos = casos_de_uso.filter(
            detalle_agil__responsable="", detalle_tradicional__actor_principal=""
        ) | casos_de_uso.filter(
            detalle_agil__isnull=True, detalle_tradicional__isnull=True
        )

        dashboard_data.append({
            "proyecto": proyecto,
            "integrantes": integrantes,
            "requerimientos": requerimientos,
            "casos_de_uso": casos_de_uso,
            "acciones": acciones,
            "reqs_huerfanos": reqs_huerfanos,
            "casos_huerfanos": casos_huerfanos,
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
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_requerimientos.html')

@login_required
def lider_casos(request):
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_casos.html')

@login_required
def lider_reportes(request):
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_reportes.html')

@login_required
def lider_priorizar(request):
    from requerimientos.models import Requerimiento
    from proyectos.models import Proyecto

    proyectos = Proyecto.objects.filter(lider=request.user)
    # Para simplicidad, priorizamos el primer proyecto liderado
    proyecto = proyectos.first() if proyectos.exists() else None
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto) if proyecto else []

    MOSCOW_CHOICES = [
        ("MUST", "Must"),
        ("SHOULD", "Should"),
        ("COULD", "Could"),
        ("WONT", "Won't")
    ]

    if request.method == "POST":
        for req in requerimientos:
            prioridad = request.POST.get(f"prioridad_{req.pk}")
            if prioridad:
                # Guardamos la prioridad en el campo 'prioridad' del detalle tradicional
                if req.detalle_tradicional:
                    req.detalle_tradicional.prioridad = prioridad
                    req.detalle_tradicional.save()
        return redirect('dashboards:lider_priorizar')

    return render(request, 'dashboards/lider_priorizar.html', {
        "proyecto": proyecto,
        "requerimientos": requerimientos,
        "MOSCOW_CHOICES": MOSCOW_CHOICES,
    })