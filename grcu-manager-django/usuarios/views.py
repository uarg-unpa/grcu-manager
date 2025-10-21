from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from accounts.models import Usuario
from roles.models import Rol
from .forms import UsuarioEditarForm, UsuarioCrearForm  

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
def buscar_usuarios_ajax(request):
    """Endpoint AJAX para búsqueda de usuarios"""
    search_query = request.GET.get('q', '').strip()
    
    if not search_query:
        return JsonResponse({'usuarios': [], 'count': 0})
    
    # Buscar en nombre y email con prefetch_related para optimizar
    usuarios = Usuario.objects.filter(
        Q(nombre__icontains=search_query) | Q(email__icontains=search_query)
    ).prefetch_related('roles').order_by('id')[:50]  # Limitar a 50 resultados
    
    # Serializar usuarios
    usuarios_data = []
    for usuario in usuarios:
        usuarios_data.append({
            'id': usuario.pk,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'avatar': usuario.avatar if usuario.avatar else None,
            'is_active': usuario.is_active,
            'roles': [rol.nombre for rol in usuario.roles.all()]
        })
    
    return JsonResponse({
        'usuarios': usuarios_data,
        'count': len(usuarios_data)
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

    # Mostrar solo roles Admin y Desarrollador para que el admin pueda asignarlos
    roles_qs = Rol.objects.filter(nombre__in=["Admin", "Desarrollador"]).order_by('nombre')
    roles = []
    for rol in roles_qs:
        roles.append((rol.nombre, None, rol.pk, rol.color, rol.icono_url))

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

    # Mostrar solo roles Admin y Desarrollador para que el admin pueda asignarlos
    roles_qs = Rol.objects.filter(nombre__in=["Admin", "Desarrollador"]).order_by('nombre')
    roles = []
    for rol in roles_qs:
        roles.append((rol.nombre, None, rol.pk, rol.color, rol.icono_url))
    
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

    # Obtener proyectos donde el usuario es líder o participante
    proyectos_como_lider = user.lidera_proyectos.all()
    proyectos_como_participante = user.proyectos.all()

    # Obtener grupos donde el usuario es líder, creador o integrante
    grupos_como_lider = user.lider_grupos.all()
    grupos_como_creador = user.grupos_creados.all()
    grupos_como_integrante = user.grupos.all()

    return render(request, "usuarios/confirmacion_eliminar_usuario.html", {
        "user": user,
        "proyectos_como_lider": proyectos_como_lider,
        "proyectos_como_participante": proyectos_como_participante,
        "grupos_como_lider": grupos_como_lider,
        "grupos_como_creador": grupos_como_creador,
        "grupos_como_integrante": grupos_como_integrante,
        "page_title": "Eliminar Usuario"
    })
