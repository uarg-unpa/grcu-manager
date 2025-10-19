from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Grupo
from accounts.models import Usuario
from .forms import GrupoForm
from django.core.paginator import Paginator
from django.db.models import Q
import json

def is_admin(user):
	return hasattr(user, 'es_admin') and user.es_admin()

@login_required
@user_passes_test(is_admin)
def api_grupo_integrantes(request, grupo_id):
    """API endpoint para obtener los integrantes de un grupo"""
    try:
        grupo = Grupo.objects.get(id=grupo_id, activo=True)
        integrantes = grupo.integrantes.all().order_by('nombre')
        data = {
            'integrantes': [
                {
                    'id': integrante.id,
                    'nombre': integrante.nombre,
                    'email': integrante.email
                }
                for integrante in integrantes
            ]
        }
        return JsonResponse(data)
    except Grupo.DoesNotExist:
        return JsonResponse({'error': 'Grupo no encontrado'}, status=404)

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

			# Asignar integrantes seleccionados
			integrantes_json = request.POST.get("integrantes_seleccionados", "[]")
			try:
				integrantes_ids = json.loads(integrantes_json)
				if integrantes_ids:
					integrantes = Usuario.objects.filter(id__in=integrantes_ids)
					grupo.integrantes.set(integrantes)
			except (json.JSONDecodeError, ValueError):
				# Si hay error en el JSON, usar el método anterior como fallback
				integrantes_ids = request.POST.getlist("integrantes")
				if integrantes_ids:
					integrantes = Usuario.objects.filter(id__in=integrantes_ids)
					grupo.integrantes.set(integrantes)

			messages.success(request, "Grupo creado correctamente.")
			return redirect("grupos:lista_grupos")
	else:
		form = GrupoForm()
	# Cargar todos los usuarios para búsqueda en tiempo real en frontend
	usuarios = Usuario.objects.all().order_by('nombre')
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Crear",
		"page_title": "Crear Grupo",
		"usuarios": usuarios,
		"integrantes_ids": [],
		"integrantes_ids_json": "[]",
	})

@login_required
@user_passes_test(is_admin)
def editar_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)
	if request.method == "POST":
		form = GrupoForm(request.POST, request.FILES, instance=grupo)
		if form.is_valid():
			grupo = form.save()

			# Asignar integrantes seleccionados
			integrantes_json = request.POST.get("integrantes_seleccionados", "[]")
			try:
				integrantes_ids = json.loads(integrantes_json)
				integrantes = Usuario.objects.filter(id__in=integrantes_ids)
				grupo.integrantes.set(integrantes)
			except (json.JSONDecodeError, ValueError):
				# Si hay error en el JSON, usar el método anterior como fallback
				integrantes_ids = request.POST.getlist("integrantes")
				integrantes = Usuario.objects.filter(id__in=integrantes_ids)
				grupo.integrantes.set(integrantes)

			messages.success(request, "Grupo actualizado correctamente.")
			return redirect("grupos:lista_grupos")
	else:
		form = GrupoForm(instance=grupo)
	# Cargar todos los usuarios para búsqueda en tiempo real en frontend
	usuarios = Usuario.objects.all().order_by('nombre')

	integrantes_ids = list(grupo.integrantes.values_list('id', flat=True))
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Editar",
		"page_title": "Editar Grupo",
		"usuarios": usuarios,
		"integrantes_ids": integrantes_ids,
		"integrantes_ids_json": json.dumps(integrantes_ids),
		"grupo": grupo,
	})

@login_required
@user_passes_test(is_admin)
def eliminar_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)

	# Verificar si el grupo tiene proyectos asignados
	from proyectos.models import Proyecto
	proyectos_asignados = Proyecto.objects.filter(grupo=grupo, activo=True)

	if request.method == "POST":
		# Si se confirma la eliminación, limpiar todas las relaciones
		for proyecto in proyectos_asignados:
			# Limpiar el líder si era integrante de este grupo
			if proyecto.lider and proyecto.lider in grupo.integrantes.all():
				proyecto.lider = None
				proyecto.save()

			# Remover todos los participantes que eran de este grupo
			participantes_a_remover = proyecto.participantes.filter(
				id__in=grupo.integrantes.values_list('id', flat=True)
			)
			for participante in participantes_a_remover:
				# Eliminar la participación en el proyecto
				from proyectos.models import ParticipacionProyecto
				ParticipacionProyecto.objects.filter(
					usuario=participante,
					proyecto=proyecto
				).delete()

		# Ahora sí eliminar el grupo
		grupo.delete()
		messages.success(request, f"Grupo '{grupo.nombre}' eliminado correctamente. Se han limpiado todas las relaciones con proyectos.")
		return redirect("grupos:lista_grupos")

	return render(request, "grupos/confirmar_eliminar_grupo.html", {
		"grupo": grupo,
		"proyectos_asignados": proyectos_asignados,
		"page_title": "Eliminar Grupo"
	})
