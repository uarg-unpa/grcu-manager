from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import Usuario 
from .forms import UsuarioEditarForm, UsuarioCrearForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


from usuarios.models import Usuario   # tu modelo de usuario
from roles.models import Rol  

# Helper para verificar si el usuario es administrador
def is_admin(user):
    return user.roles.filter(nombre__iexact="admin").exists()

@login_required
def lista_usuarios(request):
    usuarios_qs = Usuario.objects.all().order_by('id')
    paginator = Paginator(usuarios_qs, 10)  # 10 por página

    page_number = request.GET.get("page")
    usuarios = paginator.get_page(page_number)

    return render(request, "usuarios/usuario_list.html", {
        "usuarios": usuarios,
        "page_title": "Listado de Usuarios",
    })

@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.nombre = user.email  # Nombre temporal, se actualizará con Google login
            user.set_password("temporal123")
            user.save()
            form.save_m2m()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuarios:lista")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = UsuarioCrearForm()

    # Mostrar roles Admin y Desarrollador para que el admin pueda asignarlos
    roles_qs = Rol.objects.filter(nombre__in=["Admin", "Desarrollador"])
    roles = []
    for rol in roles_qs:
        if rol.nombre == "Admin":
            icon = "admin.png"
        elif rol.nombre == "Desarrollador":
            icon = "developer.png"
        else:
            icon = "default.png"
        roles.append((rol.nombre, icon, rol.pk, rol.color, rol.icono_url))

    return render(request, "usuarios/usuario_crear.html", {
        "form": form,
        "roles": roles,
        "page_title": "Crear Usuario"
    })

@login_required
@user_passes_test(is_admin)
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            messages.success(request, "Usuario actualizado correctamente.")
            # Renderizar el mismo template para mostrar el mensaje sin redirección
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = UsuarioEditarForm(instance=usuario)

    # Mostrar roles Admin y Desarrollador para que el admin pueda asignarlos
    roles_qs = Rol.objects.filter(nombre__in=["Admin", "Desarrollador"])
    roles = []
    for rol in roles_qs:
        if rol.nombre == "Admin":
            icon = "admin.png"
        elif rol.nombre == "Desarrollador":
            icon = "developer.png"
        else:
            icon = "default.png"
        roles.append((rol.nombre, icon, rol.pk, rol.color, rol.icono_url))
    return render(request, "usuarios/usuario_editar.html", {
        "form": form,
        "usuario": usuario,
        "roles": roles,
        "page_title": "Editar Usuario"
    })


@login_required
@user_passes_test(is_admin)
def eliminar_usuario(request, pk):
    user = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        user.delete()
        return redirect("usuarios:lista")  # volver a la lista de usuarios

    return render(request, "usuarios/confirmacion_eliminar_usuario.html", {
        "user": user,
        "page_title": "Eliminar Usuario"
    })
