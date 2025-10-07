from django.shortcuts import render, redirect
from accounts.models import Usuario
from roles.models import Rol
from permisos.models import Permiso
from django.contrib.auth.decorators import login_required
from proyectos.models import Proyecto
from django.contrib.admin.models import LogEntry  

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
def lider_dashboard(request):
    # Traemos los proyectos donde el usuario es líder
    proyectos = Proyecto.objects.filter(lider=request.user)

    # Si no hay proyectos, mostramos el dashboard vacío
    if not proyectos.exists():
        return render(request, "dashboards/lider_dashboard.html", {
            "proyectos": proyectos,
        })

    # Tomamos el primer proyecto liderado
    proyecto = proyectos.first()

    if proyecto is None:
        # Esto es un caso extremo, por seguridad
        return render(request, "dashboards/lider_dashboard.html", {
            "proyectos": proyectos,
        })

    # Si el proyecto no tiene metodología, redirigimos a la elección
    if not proyecto.metodologia:
        if request.method == "POST":
            metodologia = request.POST.get("metodologia")
            if metodologia:
                proyecto.metodologia = metodologia
                proyecto.save()
                return redirect("dashboards:lider_dashboard")
            

        return render(request, "dashboards/lider_eleccion_metodologia.html", {
            "proyecto": proyecto,
        })

    # Si ya tiene metodología, mostramos el dashboard
    return render(request, "dashboards/lider_dashboard.html", {
        "proyectos": proyectos,
        "page_title": "Dashboard - Lider"
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
    # Solo mostramos el HTML simulado
    return render(request, 'dashboards/lider_priorizar.html')