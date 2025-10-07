from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from proyectos.models import Proyecto, ParticipacionProyecto
from roles.models import Rol
from accounts.models import Usuario


# Helpers
def is_admin(user):
    return user.roles.filter(nombre__iexact="Admin").exists()

@login_required
@user_passes_test(is_admin)
def lista_proyectos(request):
    proyectos = Proyecto.objects.select_related('lider').all()
    return render(request, "proyectos/lista_proyectos.html", {
        "proyectos": proyectos,
        "page_title": "Lista de Proyectos"
    })


@login_required
@user_passes_test(is_admin)
def crear_proyecto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        lider_id = request.POST.get("lider")
        logo = request.FILES.get("logo")
        participantes_ids = request.POST.getlist("participantes")  # <- lista de IDs seleccionados

        lider = None
        if lider_id:
            lider = Usuario.objects.get(id=lider_id)

        proyecto = Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            lider=lider,
            creado_por=request.user,
            logo=logo
        )

        # Agregar participantes con rol por defecto (ej. Developer)
        rol_dev = Rol.objects.get(nombre="Developer")  # o lo que quieras
        for usuario_id in participantes_ids:
            usuario = Usuario.objects.get(id=usuario_id)
            ParticipacionProyecto.objects.create(
                usuario=usuario,
                proyecto=proyecto,
                rol=rol_dev
            )

        return redirect("proyectos:lista_proyectos")

    usuarios = Usuario.objects.all().distinct()
    return render(request, "proyectos/crear_proyecto.html", {
        "usuarios": usuarios,
        "page_title": "Crear Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == "POST":
        proyecto.nombre = request.POST.get("nombre")
        proyecto.descripcion = request.POST.get("descripcion")
        lider_id = request.POST.get("lider")
        logo = request.FILES.get("logo")
        participantes_ids = request.POST.getlist("participantes")  # <- lista de IDs seleccionados

        proyecto.lider = get_object_or_404(Usuario, id=lider_id)
        if logo:
            proyecto.logo = logo
        proyecto.save()

        # Actualizar participantes: borrar los antiguos y agregar los seleccionados
        proyecto.participantes.clear()
        rol_dev = Rol.objects.get(nombre="Developer")
        for usuario_id in participantes_ids:
            usuario = Usuario.objects.get(id=usuario_id)
            ParticipacionProyecto.objects.create(
                usuario=usuario,
                proyecto=proyecto,
                rol=rol_dev
            )

        messages.success(request, "Proyecto actualizado.")
        return redirect("proyectos:lista_proyectos")

    alumnos = Usuario.objects.all().distinct()
    participantes_ids = list(proyecto.participantes.values_list('id', flat=True))
    return render(request, "proyectos/editar_proyecto.html", {
        "proyecto": proyecto,
        "alumnos": alumnos,
        "participantes_ids": participantes_ids,
        "page_title": "Editar Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    messages.success(request, "Proyecto eliminado.")
    return redirect("proyectos:lista_proyectos")
