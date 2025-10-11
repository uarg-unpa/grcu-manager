from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Grupo
from accounts.models import Usuario
from .forms import GrupoForm
from django.core.paginator import Paginator
from django.db.models import Q

def is_admin(user):
	return hasattr(user, 'es_admin') and user.es_admin()

@login_required
@user_passes_test(is_admin)
def lista_grupos(request):
	grupos = Grupo.objects.all()
	# Depuración: imprimir la URL del logo de cada grupo
	for grupo in grupos:
		if grupo.logo:
			print(f"[DEPURACIÓN] Grupo: {grupo.nombre} - Logo URL: {grupo.logo.url}")
	return render(request, "grupos/lista_grupos.html", {
		"grupos": grupos,
		"page_title": "Lista de Grupos"
	})

@login_required
@user_passes_test(is_admin)
def crear_grupo(request):
	if request.method == "POST":
		form = GrupoForm(request.POST, request.FILES)
		if form.is_valid():
			grupo = form.save(commit=False)
			grupo.creado_por = request.user
			grupo.save()
			form.save_m2m()
			messages.success(request, "Grupo creado correctamente.")
			return redirect("grupos:lista_grupos")
	else:
		form = GrupoForm()
	# preparar listado de usuarios paginado (buscador compatible)
	q = request.GET.get('q', '')
	p_page = request.GET.get('p_page', 1)
	usuarios_qs = Usuario.objects.all().order_by('nombre')
	if q:
		usuarios_qs = usuarios_qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
	paginator = Paginator(usuarios_qs, 10)
	alumnos_page = paginator.get_page(p_page)
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Crear",
		"page_title": "Crear Grupo",
		"alumnos_page": alumnos_page,
		"q": q,
		"integrantes_ids": [],
	})

@login_required
@user_passes_test(is_admin)
def editar_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)
	if request.method == "POST":
		form = GrupoForm(request.POST, request.FILES, instance=grupo)
		if form.is_valid():
			form.save()
			messages.success(request, "Grupo actualizado correctamente.")
			return redirect("grupos:lista_grupos")
	else:
		form = GrupoForm(instance=grupo)
	# paginación y búsqueda para miembros (igual que en proyectos)
	q = request.GET.get('q', '')
	p_page = request.GET.get('p_page', 1)
	usuarios_qs = Usuario.objects.all().order_by('nombre')
	if q:
		usuarios_qs = usuarios_qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
	paginator = Paginator(usuarios_qs, 10)
	alumnos_page = paginator.get_page(p_page)

	integrantes_ids = list(grupo.integrantes.values_list('id', flat=True))
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Editar",
		"page_title": "Editar Grupo",
		"alumnos_page": alumnos_page,
		"q": q,
		"integrantes_ids": integrantes_ids,
		"grupo": grupo,
	})

@login_required
@user_passes_test(is_admin)
def eliminar_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)
	if request.method == "POST":
		grupo.delete()
		messages.success(request, "Grupo eliminado correctamente.")
		return redirect("grupos:lista_grupos")
	return render(request, "grupos/confirmar_eliminar_grupo.html", {
		"grupo": grupo,
		"page_title": "Eliminar Grupo"
	})
