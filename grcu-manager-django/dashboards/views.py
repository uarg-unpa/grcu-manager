from django.shortcuts import render
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
    })