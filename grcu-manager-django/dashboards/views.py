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
from requerimientos.models import Requerimiento
from casos_de_uso.models import CasoDeUso
from django.utils import timezone
from datetime import timedelta

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

    # Nuevas métricas solicitadas
    usuarios_sin_grupos = Usuario.objects.exclude(grupos__isnull=False).distinct().count()
    proyectos_sin_grupo = Proyecto.objects.filter(grupo__isnull=True).count()
    proyectos_sin_requerimientos = Proyecto.objects.annotate(
        num_requerimientos=Count('requerimientos')
    ).filter(num_requerimientos=0).count()
    
    # Proyectos actuales (creados en el año actual)
    from django.utils import timezone
    anio_actual = timezone.now().year
    proyectos_actuales = Proyecto.objects.filter(fecha_creacion__year=anio_actual).count()

    # Calcular proyectos más activos en los últimos 10 días
    fecha_limite = timezone.now() - timedelta(days=10)
    
    # Contar actividad por proyecto (requerimientos creados/modificados)
    proyectos_requerimientos = (
        Requerimiento.objects.filter(
            proyecto__activo=True,
            fecha_creacion__gte=fecha_limite
        )
        .values('proyecto__nombre')
        .annotate(actividad=Count('id'))
        .order_by('-actividad')[:4]
    )
    
    # Contar actividad por proyecto (casos de uso creados/modificados)
    proyectos_casos = (
        CasoDeUso.objects.filter(
            proyecto__activo=True,
            fecha_creacion__gte=fecha_limite
        )
        .values('proyecto__nombre')
        .annotate(actividad=Count('id'))
        .order_by('-actividad')[:4]
    )
    
    # Combinar y sumar actividades por proyecto
    actividad_proyectos = {}
    for item in proyectos_requerimientos:
        nombre = item['proyecto__nombre']
        actividad_proyectos[nombre] = actividad_proyectos.get(nombre, 0) + item['actividad']
    
    for item in proyectos_casos:
        nombre = item['proyecto__nombre']
        actividad_proyectos[nombre] = actividad_proyectos.get(nombre, 0) + item['actividad']
    
    # Obtener los 4 proyectos más activos
    proyectos_mas_activos = sorted(actividad_proyectos.items(), key=lambda x: x[1], reverse=True)[:4]
    
    # Preparar datos para el gráfico de dona
    if proyectos_mas_activos:
        proyectos_activos_labels = [proyecto[0] for proyecto in proyectos_mas_activos]
        proyectos_activos_values = [proyecto[1] for proyecto in proyectos_mas_activos]
    else:
        proyectos_activos_labels = ["Sin actividad"]
        proyectos_activos_values = [0]
    
    proyectos_activos_labels_json = json.dumps(proyectos_activos_labels)
    proyectos_activos_values_json = json.dumps(proyectos_activos_values)

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
        "usuarios_sin_grupos": usuarios_sin_grupos,
        "proyectos_sin_grupo": proyectos_sin_grupo,
        "proyectos_sin_requerimientos": proyectos_sin_requerimientos,
        "proyectos_actuales": proyectos_actuales,
        "usuarios_roles_labels": roles_labels,
        "usuarios_roles_labels_json": roles_labels_json,
        "usuarios_roles_values_json": usuarios_por_rol_json,
        "proyectos_estado_labels": proyectos_estado_labels,
        "proyectos_estado_labels_json": proyectos_estado_labels_json,
        "proyectos_estado_values_json": proyectos_estado_values_json,
        "grupos_estado_labels": grupos_estado_labels,
        "grupos_estado_labels_json": grupos_estado_labels_json,
        "grupos_estado_values_json": grupos_estado_values_json,
        "proyectos_activos_labels": proyectos_activos_labels,
        "proyectos_activos_labels_json": proyectos_activos_labels_json,
        "proyectos_activos_values_json": proyectos_activos_values_json,
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
def admin_herramientas(request):
    """
    Página de herramientas administrativas avanzadas.
    Solo accesible para administradores.
    """
    if not request.user.es_admin():
        from django.contrib import messages
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('dashboards:admin_dashboard')
    
    from django.conf import settings
    return render(request, "dashboards/admin_herramientas.html", {
        "page_title": "Herramientas Administrativas",
        "debug": settings.DEBUG,
    })


@login_required
def lider_dashboard(request):
    from requerimientos.models import Requerimiento
    from casos_de_uso.models import CasoDeUso
    from auditoria.models import RegistroActividad

    proyectos = Proyecto.objects.filter(lider=request.user)
    
    # Verificar si hay proyectos que necesitan metodología asignada
    proyecto_necesita_metodologia = proyectos.filter(metodologia__isnull=True).first()
    if proyecto_necesita_metodologia:
        from django.contrib import messages
        messages.info(request, f"El proyecto '{proyecto_necesita_metodologia.nombre}' necesita que asignes una metodología antes de continuar.")
        return redirect('proyectos:asignar_metodologia', proyecto_id=proyecto_necesita_metodologia.pk)
    
    dashboard_data = []

    for proyecto in proyectos:
        # Separar integrantes del equipo de desarrollo de los clientes
        integrantes_desarrollo = list(proyecto.participantes.exclude(id__in=proyecto.clientes.all()))
        clientes = list(proyecto.clientes.all())
        
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
        casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
        
        # Calcular totales
        total_requerimientos = requerimientos.count()
        total_casos_de_uso = casos_de_uso.count()

        # Acciones recientes de los integrantes del proyecto (solo equipo de desarrollo)
        acciones = RegistroActividad.objects.filter(usuario__in=integrantes_desarrollo).order_by('-fecha')[:20]

        # Huérfanos definidos por ausencia de relación en la tabla intermedia RequerimientoCaso
        reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
        casos_huerfanos = casos_de_uso.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
        reqs_huerfanos_count = reqs_huerfanos.count()
        casos_huerfanos_count = casos_huerfanos.count()
        reqs_huerfanos_ids = list(reqs_huerfanos.values_list('pk', flat=True))
        casos_huerfanos_ids = list(casos_huerfanos.values_list('pk', flat=True))
        total_huerfanos = reqs_huerfanos_count + casos_huerfanos_count

        reqs_relacionados = total_requerimientos - reqs_huerfanos_count
        casos_relacionados = total_casos_de_uso - casos_huerfanos_count

        # Calcular métricas adicionales de requerimientos por estado
        reqs_sin_validar = requerimientos.filter(estado='BORRADOR').count()
        reqs_completados = requerimientos.filter(estado__in=['TERMINADO', 'COMPLETADO']).count()
        reqs_sin_completar = total_requerimientos - reqs_completados

        dashboard_data.append({
            "proyecto": proyecto,
            "integrantes": integrantes_desarrollo,
            "clientes": clientes,
            "requerimientos": requerimientos,
            "casos_de_uso": casos_de_uso,
            "total_requerimientos": total_requerimientos,
            "total_casos_de_uso": total_casos_de_uso,
            "acciones": acciones,
            "reqs_huerfanos": reqs_huerfanos,
            "reqs_huerfanos_count": reqs_huerfanos_count,
            "reqs_huerfanos_ids": reqs_huerfanos_ids,
            "casos_huerfanos": casos_huerfanos,
            "casos_huerfanos_count": casos_huerfanos_count,
            "casos_huerfanos_ids": casos_huerfanos_ids,
            "total_huerfanos": total_huerfanos,
            "reqs_relacionados": reqs_relacionados,
            "casos_relacionados": casos_relacionados,
            "reqs_sin_validar": reqs_sin_validar,
            "reqs_completados": reqs_completados,
            "reqs_sin_completar": reqs_sin_completar,
            "necesita_metodologia": proyecto.necesita_metodologia(),  # ⚡ NUEVO
            "puede_cambiar_metodologia": proyecto.puede_cambiar_metodologia(),  # ⚡ NUEVO
        })

    # Obtener el primer proyecto para el título
    primer_proyecto = proyectos.first()
    titulo_proyecto = primer_proyecto.nombre if primer_proyecto else "Sin Proyecto"
    
    return render(request, "dashboards/lider_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": f"{titulo_proyecto} - Dashboard - Líder"
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
    
    # Obtener el primer proyecto para el título
    primer_proyecto = proyectos.first()
    titulo_proyecto = primer_proyecto.nombre if primer_proyecto else "Sin Proyecto"
    
    return render(request, "dashboards/developer_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": f"{titulo_proyecto} - Developer Dashboard",
        "proyecto": primer_proyecto,
    })

@login_required
def developer_matriz(request):
    """
    Redirige a la matriz de trazabilidad del primer proyecto del desarrollador.
    La matriz ahora está en la app proyectos donde corresponde.
    """
    from django.contrib import messages
    
    proyectos = Proyecto.objects.filter(participantes=request.user)
    
    proyecto_id = request.GET.get('proyecto')
    if proyecto_id:
        proyecto = proyectos.filter(id=proyecto_id).first()
    else:
        proyecto = proyectos.first()
    
    if not proyecto:
        messages.error(request, 'No participas en ningún proyecto actualmente.')
        return redirect('dashboards:developer_dashboard')
    
    # Redirigir a la matriz del proyecto
    return redirect('proyectos:matriz_trazabilidad', proyecto_id=proyecto.pk)

@login_required
def stakeholder_dashboard(request):
    """
    Dashboard para clientes/stakeholders.
    Muestra los proyectos donde el usuario es cliente.
    Los clientes pueden ver requerimientos pero no editarlos.
    """
    from requerimientos.models import Requerimiento
    from casos_de_uso.models import CasoDeUso
    
    # Obtener proyectos donde el usuario es cliente
    proyectos = Proyecto.objects.filter(clientes=request.user)
    dashboard_data = []
    
    for proyecto in proyectos:
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
        casos_de_uso = CasoDeUso.objects.filter(proyecto=proyecto)
        
        # Calcular huérfanos
        reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
        casos_huerfanos = casos_de_uso.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
        
        reqs_relacionados = requerimientos.count() - reqs_huerfanos.count()
        casos_relacionados = casos_de_uso.count() - casos_huerfanos.count()
        
        # Métricas por estado
        reqs_pendientes = requerimientos.filter(estado='BORRADOR').count()
        reqs_validados = requerimientos.filter(estado='VALIDADO').count()
        reqs_completados = requerimientos.filter(estado__in=['TERMINADO', 'COMPLETADO']).count()
        
        dashboard_data.append({
            "proyecto": proyecto,
            "requerimientos": requerimientos,
            "casos_de_uso": casos_de_uso,
            "reqs_huerfanos": reqs_huerfanos,
            "casos_huerfanos": casos_huerfanos,
            "reqs_relacionados": reqs_relacionados,
            "casos_relacionados": casos_relacionados,
            "reqs_pendientes": reqs_pendientes,
            "reqs_validados": reqs_validados,
            "reqs_completados": reqs_completados,
        })
    
    # Obtener el primer proyecto para el título
    primer_proyecto = proyectos.first()
    titulo_proyecto = primer_proyecto.nombre if primer_proyecto else "Sin Proyecto"
    
    return render(request, "dashboards/stakeholder_dashboard.html", {
        "dashboard_data": dashboard_data,
        "page_title": f"{titulo_proyecto} - Dashboard Cliente",
    })


@login_required
def limpiar_base_datos(request):
    """
    Limpia la base de datos eliminando todas las entradas de las tablas seleccionadas
    o realizando un reset completo usando el comando reset_data.
    Esta vista es solo para propósitos de desarrollo y pruebas.
    """
    from django.contrib import messages
    from django.db import transaction
    from django.core.management import call_command
    from django.conf import settings
    
    # Verificar que sea administrador (usando el sistema de roles personalizado)
    if not request.user.es_admin():
        messages.error(request, "No tienes permisos para realizar esta acción. Se requiere rol de Administrador.")
        return redirect('dashboards:admin_herramientas')
    
    if request.method == "POST":
        tipo_limpieza = request.POST.get("tipo_limpieza")
        
        if tipo_limpieza == "reset_completo":
            # Usar el comando reset_data.py de la app core
            if not settings.DEBUG:
                messages.error(request, "El reset completo solo puede ejecutarse en modo DEBUG.")
                return redirect('dashboards:admin_herramientas')
            
            # Confirmar la acción
            if "confirmar" in request.POST:
                try:
                    # Ejecutar el comando reset_data con --force (sin confirmación interactiva)
                    call_command('reset_data', force=True, verbosity=2)
                    messages.success(request, "Base de datos reseteada completamente usando el comando reset_data.")
                except Exception as e:
                    messages.error(request, f"Ocurrió un error al resetear la base de datos: {str(e)}")
            else:
                return render(request, "dashboards/confirmar_reset_completo.html", {})
        
        elif tipo_limpieza == "limpiar_tablas":
            # Lógica original de limpiar tablas específicas
            tablas = request.POST.getlist("tablas")
            
            # Asegurarse de que al menos una tabla esté seleccionada
            if not tablas:
                messages.error(request, "Debes seleccionar al menos una tabla para limpiar.")
                return redirect('dashboards:admin_herramientas')
            
            # Confirmar la acción
            if "confirmar" in request.POST:
                try:
                    with transaction.atomic():
                        for tabla in tablas:
                            if tabla == "usuarios":
                                Usuario.objects.all().delete()
                            elif tabla == "proyectos":
                                Proyecto.objects.all().delete()
                            elif tabla == "grupos":
                                Grupo.objects.all().delete()
                                
                    messages.success(request, "Base de datos limpiada exitosamente.")
                except Exception as e:
                    messages.error(request, f"Ocurrió un error al limpiar la base de datos: {str(e)}")
            else:
                return render(request, "dashboards/confirmar_limpiar_bd.html", {"tablas": tablas})
        
        else:
            messages.error(request, "Tipo de limpieza no válido.")
    
    return redirect('dashboards:admin_herramientas')

