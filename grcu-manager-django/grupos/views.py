from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Grupo
from accounts.models import Usuario
from .forms import GrupoForm

def is_admin(user):
	return hasattr(user, 'es_admin') and user.es_admin()

@login_required
@user_passes_test(is_admin)
def lista_grupos(request):
	grupos = Grupo.objects.all()
	return render(request, "grupos/lista_grupos.html", {"grupos": grupos})

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
	return render(request, "grupos/form_grupo.html", {"form": form, "accion": "Crear"})

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
	return render(request, "grupos/form_grupo.html", {"form": form, "accion": "Editar"})

@login_required
@user_passes_test(is_admin)
def eliminar_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)
	if request.method == "POST":
		grupo.delete()
		messages.success(request, "Grupo eliminado correctamente.")
		return redirect("grupos:lista_grupos")
	return render(request, "grupos/confirmar_eliminar_grupo.html", {"grupo": grupo})
