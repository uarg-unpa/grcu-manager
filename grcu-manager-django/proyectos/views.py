from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from proyectos.models import Proyecto, ParticipacionProyecto
from roles.models import Rol
from accounts.models import Usuario
from django.core.paginator import Paginator
from django.db.models import Q


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

        # Agregar participantes con rol por defecto (Desarrollador)
        # Usamos get_or_create para evitar errores si el rol no existe
        rol_dev, _ = Rol.objects.get_or_create(nombre="Desarrollador", defaults={"color": "#ffc107"})
        for usuario_id in participantes_ids:
            usuario = Usuario.objects.get(id=usuario_id)
            ParticipacionProyecto.objects.create(
                usuario=usuario,
                proyecto=proyecto,
                rol=rol_dev
            )

        return redirect("proyectos:lista_proyectos")

    # Lista de participantes con búsqueda y paginación
    q = request.GET.get('q', '').strip()
    p_page = request.GET.get('p_page')
    usuarios_qs = Usuario.objects.all().distinct().order_by('id')
    if q:
        usuarios_qs = usuarios_qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
    paginator = Paginator(usuarios_qs, 10)
    participantes_page = paginator.get_page(p_page)

    usuarios_all = Usuario.objects.all().order_by('nombre')
    return render(request, "proyectos/crear_proyecto.html", {
        "usuarios_page": participantes_page,
        "usuarios_all": usuarios_all,
        "participantes_ids": [],
        "q": q,
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
        rol_dev, _ = Rol.objects.get_or_create(nombre="Desarrollador", defaults={"color": "#ffc107"})
        for usuario_id in participantes_ids:
            usuario = Usuario.objects.get(id=usuario_id)
            ParticipacionProyecto.objects.create(
                usuario=usuario,
                proyecto=proyecto,
                rol=rol_dev
            )

        messages.success(request, "Proyecto actualizado.")
        return redirect("proyectos:lista_proyectos")

    # Lista de participantes con búsqueda y paginación
    q = request.GET.get('q', '').strip()
    p_page = request.GET.get('p_page')
    alumnos_qs = Usuario.objects.all().distinct().order_by('id')
    if q:
        alumnos_qs = alumnos_qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
    paginator = Paginator(alumnos_qs, 10)
    alumnos_page = paginator.get_page(p_page)

    participantes_ids = list(proyecto.participantes.values_list('id', flat=True))
    usuarios_all = Usuario.objects.all().order_by('nombre')
    return render(request, "proyectos/editar_proyecto.html", {
        "proyecto": proyecto,
        "alumnos_page": alumnos_page,
        "usuarios_all": usuarios_all,
        "participantes_ids": participantes_ids,
        "q": q,
        "page_title": "Editar Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    messages.success(request, "Proyecto eliminado.")
    return redirect("proyectos:lista_proyectos")
