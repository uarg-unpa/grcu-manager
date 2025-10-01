from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import Usuario 
from .forms import UsuarioEditarForm, UsuarioCrearForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from usuarios.models import Usuario   # tu modelo de usuario
from roles.models import Rol  

# Helper para verificar si el usuario es administrador
def is_admin(user):
    return user.roles.filter(nombre__iexact="Admin").exists()

@login_required
def lista_usuarios(request):
    usuarios_list = Usuario.objects.all().order_by("id")  # ordenados por ID
    paginator = Paginator(usuarios_list, 10)  # 10 por página

    page_number = request.GET.get("page")
    usuarios = paginator.get_page(page_number)

    return render(request, "usuarios/usuario_list.html", {"usuarios": usuarios})

@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password("temporal123")
            user.save()
            form.save_m2m()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuarios:lista")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = UsuarioCrearForm()

    # Solo mostrar roles permitidos para el admin
    roles = [
        ("Admin", "admin.png"),
        ("Líder", "lider.png"),
        ("Visitante", "visitante.png"),
    ]

    return render(request, "usuarios/usuario_crear.html", {"form": form, "roles": roles})

@login_required
@user_passes_test(is_admin)
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            # No tocamos email si no se quiere editar
            user.save()
            form.save_m2m()  # Guardamos roles
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("usuarios:lista")
    else:
        form = UsuarioEditarForm(instance=usuario)

    # Solo mostrar roles permitidos para el admin
    roles = [
        ("Admin", "admin.png"),
        ("Líder", "lider.png"),
        ("Visitante", "visitante.png"),
    ]
    return render(request, "usuarios/usuario_editar.html", {"form": form, "usuario": usuario, "roles": roles})


@login_required
@user_passes_test(is_admin)
def eliminar_usuario(request, pk):
    user = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        user.delete()
        return redirect("usuarios:lista")  # volver a la lista de usuarios

    return render(request, "usuarios/confirmacion_eliminar_usuario.html", {"user": user})
