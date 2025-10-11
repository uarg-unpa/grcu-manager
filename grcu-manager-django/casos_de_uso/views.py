from django.shortcuts import render, get_object_or_404, redirect
from .models import CasoDeUso
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required

@login_required
def caso_de_uso_list(request, proyecto_id=None):
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        casos = CasoDeUso.objects.filter(proyecto=proyecto)
    else:
        # Si el usuario es líder, mostrar solo el primer proyecto que lidera
        proyectos_liderados = getattr(request.user, 'lidera_proyectos', None)
        if proyectos_liderados and proyectos_liderados.exists():
            proyecto = proyectos_liderados.first()
            casos = CasoDeUso.objects.filter(proyecto=proyecto)
        else:
            casos = CasoDeUso.objects.all()
            proyecto = None
    if proyecto:
        page_title = f"{proyecto.nombre} - Casos de Uso"
    else:
        page_title = "Casos de Uso"
    return render(request, "casos_de_uso/caso_de_uso_list.html", {"casos": casos, "proyecto": proyecto, "page_title": page_title})

@login_required
def caso_de_uso_detail(request, pk):
    caso = get_object_or_404(CasoDeUso, pk=pk)
    return render(request, "casos_de_uso/caso_de_uso_detail.html", {"caso": caso})
