from django.shortcuts import render, get_object_or_404, redirect
from .models import Requerimiento
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required

@login_required
def requerimiento_list(request, proyecto_id=None):
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    else:
        requerimientos = Requerimiento.objects.all()
        proyecto = None
    return render(request, "requerimientos/requerimiento_list.html", {"requerimientos": requerimientos, "proyecto": proyecto})

@login_required
def requerimiento_detail(request, pk):
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    return render(request, "requerimientos/requerimiento_detail.html", {"requerimiento": requerimiento})
