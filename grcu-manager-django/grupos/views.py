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
from django.http import JsonResponse

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
	# Obtener parámetro de ordenamiento
	sort = request.GET.get('sort', '-id')  # Por defecto, último creado primero
	
	# Mapeo de valores válidos
	valid_sorts = {
		'nombre': 'nombre',
		'-nombre': '-nombre',
		'integrantes': 'integrantes',
		'-integrantes': '-integrantes',
		'activo': 'activo',
		'-activo': '-activo',
		'-id': '-id',
		'id': 'id',
	}
	
	# Validar sort
	if sort not in valid_sorts:
		sort = '-id'
	
	# Ordenamiento especial para integrantes (count)
	if sort in ['integrantes', '-integrantes']:
		from django.db.models import Count
		grupos_qs = Grupo.objects.annotate(num_integrantes=Count('integrantes'))
		if sort == 'integrantes':
			grupos_qs = grupos_qs.order_by('num_integrantes', 'nombre')
		else:
			grupos_qs = grupos_qs.order_by('-num_integrantes', 'nombre')
	else:
		grupos_qs = Grupo.objects.all().order_by(sort)
	
	# Paginación
	paginator = Paginator(grupos_qs, 10)
	page_number = request.GET.get('page')
	grupos = paginator.get_page(page_number)
	
	return render(request, "grupos/lista_grupos.html", {
		"grupos": grupos,
		"page_title": "Lista de Grupos",
		"sort": sort,
	})


@login_required
@user_passes_test(is_admin)
def buscar_grupos_ajax(request):
	"""Endpoint AJAX para búsqueda de grupos"""
	q = request.GET.get('q', '').strip()
	if not q:
		return JsonResponse({'grupos': [], 'count': 0})

	grupos_qs = Grupo.objects.filter(
		Q(nombre__icontains=q) |
		Q(integrantes__nombre__icontains=q)
	).prefetch_related('integrantes').distinct()[:50]

	resultados = []
	for g in grupos_qs:
		resultados.append({
			'id': g.id,
			'nombre': g.nombre,
			'logo': g.logo.url if g.logo else None,
			'integrantes': [u.nombre for u in g.integrantes.all()],
			'activo': bool(g.activo),
		})

	return JsonResponse({'grupos': resultados, 'count': len(resultados)})

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
					# Validar que ningún usuario seleccionado esté en otro grupo activo
					usuarios_en_otros_grupos = []
					for user_id in integrantes_ids:
						usuario = Usuario.objects.get(id=user_id)
						grupo_actual = Grupo.objects.filter(integrantes=usuario, activo=True).exclude(id=grupo.id).first()
						if grupo_actual:
							usuarios_en_otros_grupos.append(f"{usuario.nombre} (en '{grupo_actual.nombre}')")
					
					if usuarios_en_otros_grupos:
						grupo.delete()  # Eliminar el grupo creado
						messages.error(
							request,
							f"No se puede crear el grupo. Los siguientes usuarios ya están en grupos activos: {', '.join(usuarios_en_otros_grupos)}"
						)
						return redirect("grupos:crear_grupo")
					
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
	
	# Cargar todos los usuarios y anotar si están en un grupo activo
	usuarios = Usuario.objects.all().order_by('nombre')
	usuarios_con_info = []
	for usuario in usuarios:
		grupo_actual = Grupo.objects.filter(integrantes=usuario, activo=True).first()
		usuarios_con_info.append({
			'usuario': usuario,
			'grupo_actual': grupo_actual,
			'disponible': grupo_actual is None
		})
	
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Crear",
		"page_title": "Crear Grupo",
		"usuarios_con_info": usuarios_con_info,
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
				
				# Validar que ningún usuario seleccionado esté en otro grupo activo
				usuarios_en_otros_grupos = []
				for user_id in integrantes_ids:
					usuario = Usuario.objects.get(id=user_id)
					grupo_actual = Grupo.objects.filter(integrantes=usuario, activo=True).exclude(id=grupo.id).first()
					if grupo_actual:
						usuarios_en_otros_grupos.append(f"{usuario.nombre} (en '{grupo_actual.nombre}')")
				
				if usuarios_en_otros_grupos:
					messages.error(
						request,
						f"No se puede actualizar el grupo. Los siguientes usuarios ya están en grupos activos: {', '.join(usuarios_en_otros_grupos)}"
					)
					return redirect("grupos:editar_grupo", grupo_id=grupo_id)
				
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
	
	# Cargar todos los usuarios y anotar si están en un grupo activo
	usuarios = Usuario.objects.all().order_by('nombre')
	usuarios_con_info = []
	for usuario in usuarios:
		grupo_actual = Grupo.objects.filter(integrantes=usuario, activo=True).exclude(id=grupo.id).first()
		usuarios_con_info.append({
			'usuario': usuario,
			'grupo_actual': grupo_actual,
			'disponible': grupo_actual is None or usuario in grupo.integrantes.all()  # Disponible si no está en grupo o ya está en este grupo
		})

	integrantes_ids = list(grupo.integrantes.values_list('id', flat=True))
	return render(request, "grupos/form_grupo.html", {
		"form": form,
		"accion": "Editar",
		"page_title": "Editar Grupo",
		"usuarios_con_info": usuarios_con_info,
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
