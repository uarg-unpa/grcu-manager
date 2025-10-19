from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from proyectos.models import Proyecto, ParticipacionProyecto
from proyectos.forms import ProyectoCrearForm
from roles.models import Rol
from accounts.models import Usuario
from grupos.models import Grupo
from django.core.paginator import Paginator
from django.db.models import Q


# Helpers
def is_admin(user):
    return user.roles.filter(nombre__iexact="Admin").exists()

@login_required
@user_passes_test(is_admin)
def lista_proyectos(request):
    proyectos = Proyecto.objects.select_related('lider', 'grupo').all()
    return render(request, "proyectos/lista_proyectos.html", {
        "proyectos": proyectos,
        "page_title": "Lista de Proyectos"
    })


@login_required
@user_passes_test(is_admin)
def crear_proyecto(request):
    if request.method == "POST":
        form = ProyectoCrearForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el proyecto
            proyecto = form.save(commit=False)
            proyecto.creado_por = request.user
            proyecto.save()

            # Obtener el grupo seleccionado (puede ser None)
            grupo = proyecto.grupo

            if grupo:
                # Solo procesar líder y participantes si hay grupo
                lider_id = form.cleaned_data.get('lider')
                if lider_id:
                    lider = Usuario.objects.get(id=lider_id)

                    # Crear rol "Líder" si no existe
                    rol_lider, _ = Rol.objects.get_or_create(
                        nombre="Líder",
                        defaults={"color": "#28a745"}
                    )

                    # Asignar líder al proyecto
                    proyecto.lider = lider
                    proyecto.save()

                    # Agregar líder con rol "Líder"
                    ParticipacionProyecto.objects.create(
                        usuario=lider,
                        proyecto=proyecto,
                        rol=rol_lider
                    )

                    # Agregar todos los demás integrantes del grupo como "Desarrollador"
                    rol_dev, _ = Rol.objects.get_or_create(
                        nombre="Desarrollador",
                        defaults={"color": "#ffc107"}
                    )

                    for integrante in grupo.integrantes.exclude(id=lider_id):
                        ParticipacionProyecto.objects.create(
                            usuario=integrante,
                            proyecto=proyecto,
                            rol=rol_dev
                        )

                messages.success(request, f"Proyecto '{proyecto.nombre}' creado exitosamente con el grupo '{grupo.nombre}'.")
            else:
                # Proyecto sin grupo
                messages.success(request, f"Proyecto '{proyecto.nombre}' creado exitosamente sin grupo asignado.")

            return redirect("proyectos:lista_proyectos")
    else:
        form = ProyectoCrearForm()

    return render(request, "proyectos/crear_proyecto.html", {
        "form": form,
        "page_title": "Crear Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == "POST":
        form = ProyectoCrearForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            proyecto = form.save()

            # Obtener el grupo seleccionado (puede ser None)
            grupo = proyecto.grupo

            if grupo:
                # Solo procesar líder y participantes si hay grupo
                lider_id = form.cleaned_data.get('lider')
                if lider_id:
                    lider = Usuario.objects.get(id=lider_id)

                    # Crear rol "Líder" si no existe
                    rol_lider, _ = Rol.objects.get_or_create(
                        nombre="Líder",
                        defaults={"color": "#28a745"}
                    )

                    # Asignar líder al proyecto
                    proyecto.lider = lider
                    proyecto.save()

                    # Limpiar participantes actuales
                    proyecto.participantes.clear()

                    # Agregar líder con rol "Líder"
                    ParticipacionProyecto.objects.create(
                        usuario=lider,
                        proyecto=proyecto,
                        rol=rol_lider
                    )

                    # Agregar todos los demás integrantes del grupo como "Desarrollador"
                    rol_dev, _ = Rol.objects.get_or_create(
                        nombre="Desarrollador",
                        defaults={"color": "#ffc107"}
                    )

                    for integrante in grupo.integrantes.exclude(id=lider_id):
                        ParticipacionProyecto.objects.create(
                            usuario=integrante,
                            proyecto=proyecto,
                            rol=rol_dev
                        )

                messages.success(request, f"Proyecto '{proyecto.nombre}' actualizado exitosamente con el grupo '{grupo.nombre}'.")
            else:
                # Proyecto sin grupo - limpiar líder y participantes
                proyecto.lider = None
                proyecto.save()
                proyecto.participantes.clear()
                messages.success(request, f"Proyecto '{proyecto.nombre}' actualizado exitosamente sin grupo asignado.")

            return redirect("proyectos:lista_proyectos")
    else:
        form = ProyectoCrearForm(instance=proyecto)

    return render(request, "proyectos/editar_proyecto.html", {
        "form": form,
        "proyecto": proyecto,
        "page_title": "Editar Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    messages.success(request, "Proyecto eliminado.")
    return redirect("proyectos:lista_proyectos")
