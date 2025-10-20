from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil
from .forms import CasoDeUsoTradicionalForm, CasoDeUsoAgilForm
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

@login_required
def caso_de_uso_list(request, proyecto_id=None):
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        casos = CasoDeUso.objects.filter(proyecto=proyecto)
    else:
        # Si el usuario es líder, mostrar solo el primer proyecto que lidera
        proyectos_liderados = getattr(request.user, 'lidera_proyectos', None)
        if proyectos_liderados and proyectos_liderados.exists():
            proyecto = proyectos_liderados.first()
            casos = CasoDeUso.objects.filter(proyecto=proyecto)
        else:
            casos = CasoDeUso.objects.all()
            proyecto = None
    if proyecto:
        page_title = f"{proyecto.nombre} - Casos de Uso"
    else:
        page_title = "Casos de Uso"
    return render(request, "casos_de_uso/caso_de_uso_list.html", {"casos": casos, "proyecto": proyecto, "page_title": page_title})

@login_required
def caso_de_uso_detail(request, pk):
    caso = get_object_or_404(CasoDeUso, pk=pk)
    return render(request, "casos_de_uso/caso_de_uso_detail.html", {"caso": caso})


@login_required
def caso_de_uso_create(request, proyecto_id=None):
    """
    Vista para crear casos de uso según la metodología del proyecto.
    Puede recibir un requerimiento_id por GET para asociarlo automáticamente.
    """
    # Obtener el proyecto
    if not proyecto_id:
        messages.error(request, 'Debe especificar un proyecto para crear un caso de uso.')
        return redirect('dashboards:lider_dashboard')
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener requerimiento si se pasa por parámetro GET
    requerimiento_id = request.GET.get('requerimiento_id')
    requerimiento = None
    if requerimiento_id:
        from requerimientos.models import Requerimiento
        requerimiento = get_object_or_404(Requerimiento, id=requerimiento_id, proyecto=proyecto)
    
    # Validación 1: El proyecto debe tener metodología asignada
    if proyecto.necesita_metodologia():
        messages.error(
            request,
            f'El proyecto "{proyecto.nombre}" aún no tiene metodología asignada.'
        )
        return redirect('dashboards:lider_dashboard')
    
    # Validación 2: Verificar permisos (líder o participante del proyecto)
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    
    if not (es_lider or es_participante):
        messages.error(
            request,
            'No tienes permiso para crear casos de uso en este proyecto.'
        )
        return redirect('dashboards:lider_dashboard')
    
    # Determinar formulario según metodología
    es_tradicional = proyecto.metodologia == 'TRADICIONAL'
    es_agil = proyecto.metodologia == 'AGIL'
    
    if request.method == 'POST':
        # Instanciar el formulario apropiado
        if es_tradicional:
            form = CasoDeUsoTradicionalForm(request.POST, request.FILES)
        elif es_agil:
            form = CasoDeUsoAgilForm(request.POST, request.FILES)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('dashboards:lider_dashboard')
        
        if form.is_valid():
            # Crear el caso de uso base
            caso = CasoDeUso(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                proyecto=proyecto,
                creado_por=request.user,
                imagen=form.cleaned_data.get('imagen'),
                link_externo=form.cleaned_data.get('link_externo', '')
            )
            caso.save()
            
            # Asociar con el requerimiento si se especificó
            if requerimiento:
                from requerimientos.models import RequerimientoCaso
                RequerimientoCaso.objects.create(
                    requerimiento=requerimiento,
                    caso_de_uso=caso
                )
            
            # Crear el detalle específico según la metodología
            if es_tradicional:
                DetalleCasoDeUsoTradicional.objects.create(
                    caso_de_uso_padre=caso,
                    actor_principal=form.cleaned_data.get('actor_principal', ''),
                    precondiciones=form.cleaned_data.get('precondiciones', ''),
                    flujo_principal=form.cleaned_data.get('flujo_principal', ''),
                    flujo_alternativo=form.cleaned_data.get('flujo_alternativo', ''),
                    postcondiciones=form.cleaned_data.get('postcondiciones', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                if requerimiento:
                    messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado y asociado al requerimiento "{requerimiento.nombre}".')
                else:
                    messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado exitosamente.')
                
            elif es_agil:
                DetalleCasoDeUsoAgil.objects.create(
                    caso_de_uso_padre=caso,
                    historia_usuario=form.cleaned_data.get('historia_usuario', ''),
                    criterio_aceptacion=form.cleaned_data.get('criterio_aceptacion', ''),
                    responsable=form.cleaned_data.get('responsable', ''),
                    estado_scrum=form.cleaned_data.get('estado_scrum', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                if requerimiento:
                    messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado y asociado al requerimiento "{requerimiento.nombre}".')
                else:
                    messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado exitosamente.')
            
            # Redirigir de vuelta a la lista de requerimientos si venimos desde allí
            if requerimiento:
                return redirect(f"{reverse('requerimientos:requerimiento_list')}?proyecto_id={proyecto.pk}")
            return redirect('dashboards:lider_dashboard')
    else:
        # GET: Instanciar formulario vacío
        if es_tradicional:
            form = CasoDeUsoTradicionalForm()
        elif es_agil:
            form = CasoDeUsoAgilForm()
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('dashboards:lider_dashboard')
    
    if requerimiento:
        page_title = f"Crear Caso de Uso para Requerimiento: {requerimiento.nombre}"
    else:
        page_title = f"Crear Caso de Uso - {proyecto.nombre}"
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'requerimiento': requerimiento,
        'es_tradicional': es_tradicional,
        'es_agil': es_agil,
        'metodologia_display': proyecto.get_metodologia_display(),
        'page_title': page_title
    }
    
    return render(request, 'casos_de_uso/caso_de_uso_create.html', context)


@login_required
def buscar_casos_de_uso_ajax(request):
    """Endpoint AJAX para búsqueda de casos de uso"""
    search_query = request.GET.get('q', '').strip()
    proyecto_id = request.GET.get('proyecto_id', '').strip()
    tipo_detalle = request.GET.get('tipo_detalle', '').strip()  # 'tradicional' o 'agil'
    
    # Construir filtros
    filtros = Q()
    
    if search_query:
        filtros &= (
            Q(nombre__icontains=search_query) | 
            Q(descripcion__icontains=search_query)
        )
    
    if proyecto_id:
        filtros &= Q(proyecto_id=proyecto_id)
    
    # Filtro por tipo de detalle
    if tipo_detalle == 'tradicional':
        filtros &= Q(detalle_tradicional__isnull=False)
    elif tipo_detalle == 'agil':
        filtros &= Q(detalle_agil__isnull=False)
    
    # Si no hay filtros, devolver vacío
    if not (search_query or proyecto_id or tipo_detalle):
        return JsonResponse({'casos': [], 'count': 0})
    
    # Buscar casos de uso con prefetch_related para optimizar
    casos = CasoDeUso.objects.filter(filtros).select_related(
        'proyecto', 'detalle_tradicional', 'detalle_agil'
    ).prefetch_related('requerimientos_relacionados').order_by('nombre')[:100]
    
    # Serializar casos de uso
    casos_data = []
    for caso in casos:
        # Truncar descripción
        descripcion = caso.descripcion if caso.descripcion else ''
        if len(descripcion) > 60:
            descripcion = descripcion[:57] + '...'
        
        # Determinar tipo de detalle
        tipo = 'sin_tipo'
        if hasattr(caso, 'detalle_tradicional') and caso.detalle_tradicional:
            tipo = 'tradicional'
        elif hasattr(caso, 'detalle_agil') and caso.detalle_agil:
            tipo = 'agil'
        
        # Obtener requerimientos relacionados
        requerimientos = []
        for req in caso.requerimientos_relacionados.all():  # type: ignore[attr-defined]
            requerimientos.append({
                'id': req.pk,
                'nombre': req.nombre
            })
        
        casos_data.append({
            'id': caso.pk,
            'nombre': caso.nombre,
            'descripcion': descripcion,
            'tipo': tipo,
            'requerimientos': requerimientos
        })
    
    return JsonResponse({
        'casos': casos_data,
        'count': len(casos_data)
    })
