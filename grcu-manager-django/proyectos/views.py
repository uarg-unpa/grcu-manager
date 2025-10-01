from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Proyecto
from accounts.models import Usuario

# Helpers
def is_admin(user):
    return user.roles.filter(nombre__iexact="Admin").exists()

@login_required
@user_passes_test(is_admin)
def lista_proyectos(request):
    proyectos = Proyecto.objects.select_related('lider').all()
    return render(request, "proyectos/lista_proyectos.html", {"proyectos": proyectos})


@login_required
@user_passes_test(is_admin)
def crear_proyecto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        lider_id = request.POST.get("lider")
        logo = request.FILES.get("logo")

        lider = None
        if lider_id:
            lider = Usuario.objects.get(id=lider_id)

        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            lider=lider,
            creado_por=request.user,
            logo=logo
        )

        return redirect("proyectos:lista_proyectos")

    usuarios = Usuario.objects.all().distinct()
    return render(request, "proyectos/crear_proyecto.html", {"usuarios": usuarios})


@login_required
@user_passes_test(is_admin)
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == "POST":
        proyecto.nombre = request.POST.get("nombre")
        proyecto.descripcion = request.POST.get("descripcion")
        lider_id = request.POST.get("lider")
        logo = request.FILES.get("logo")

        proyecto.lider = get_object_or_404(Usuario, id=lider_id)
        if logo:
            proyecto.logo = logo  # Sobreescribe la imagen anterior
        proyecto.save()

        messages.success(request, "Proyecto actualizado.")
        return redirect("proyectos:lista_proyectos")

    alumnos = Usuario.objects.all().distinct()
    return render(request, "proyectos/editar_proyecto.html", {"proyecto": proyecto, "alumnos": alumnos})


@login_required
@user_passes_test(is_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    messages.success(request, "Proyecto eliminado.")
    return redirect("proyectos:lista_proyectos")
