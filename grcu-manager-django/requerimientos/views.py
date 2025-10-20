from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Requerimiento
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required
from .forms import RequerimientoForm, RequerimientoTradicionalForm, RequerimientoAgilForm
from requerimientos.models import DetalleRequerimientoTradicional, DetalleRequerimientoAgil
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

@login_required
def requerimiento_list(request, proyecto_id=None):
    from django.db.models import Count
    
    # Allow passing proyecto_id via URL param or querystring
    if not proyecto_id:
        proyecto_id = request.GET.get('proyecto_id')

    # Si es un líder y no se especifica proyecto, usar sus proyectos
    if not proyecto_id and hasattr(request.user, 'lidera_proyectos'):
        proyectos_liderados = request.user.lidera_proyectos.all()
        if proyectos_liderados.exists():
            proyecto_id = proyectos_liderados.first().pk

    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        requerimientos = Requerimiento.objects.filter(proyecto=proyecto).select_related('proyecto')
        
        # Estadísticas adicionales para líderes
        stats = None
        if request.user == proyecto.lider:
            from casos_de_uso.models import CasoDeUso
            from requerimientos.models import RequerimientoCaso
            
            casos = CasoDeUso.objects.filter(proyecto=proyecto)
            
            # Calcular huérfanos (sin relaciones)
            reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
            casos_huerfanos = casos.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
            
            # Estadísticas por estado y tipo
            req_estado_qs = requerimientos.values('estado').annotate(count=Count('id'))
            req_tipo_qs = requerimientos.values('tipo').annotate(count=Count('id'))
            
            stats = {
                'total_requerimientos': requerimientos.count(),
                'total_casos': casos.count(),
                'reqs_huerfanos': reqs_huerfanos.count(),
                'casos_huerfanos': casos_huerfanos.count(),
                'req_por_estado': list(req_estado_qs),
                'req_por_tipo': list(req_tipo_qs),
            }
    else:
        requerimientos = Requerimiento.objects.all().select_related('proyecto')
        proyecto = None
        stats = None
        
    if proyecto:
        page_title = f"{proyecto.nombre} - Requerimientos"
    else:
        page_title = "Requerimientos"

    context = {
        "requerimientos": requerimientos,
        "proyecto": proyecto,
        "stats": stats,
        "is_lider": proyecto and request.user == proyecto.lider if proyecto else False,
        "page_title": page_title,
    }
    return render(request, "requerimientos/requerimiento_list.html", context)

@login_required
def requerimiento_detail(request, pk):
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    return render(request, "requerimientos/requerimiento_detail.html", {"requerimiento": requerimiento})


@login_required
def requerimiento_create(request, proyecto_id=None):
    """
    Vista inteligente que crea requerimientos según la metodología del proyecto.
    - Si es TRADICIONAL: usa RequerimientoTradicionalForm
    - Si es ÁGIL: usa RequerimientoAgilForm
    - Valida permisos: solo líder o developers del proyecto
    """
    # Obtener el proyecto
    if not proyecto_id:
        messages.error(request, 'Debe especificar un proyecto para crear un requerimiento.')
        return redirect('dashboards:lider_dashboard')
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Validación 1: El proyecto debe tener metodología asignada
    if proyecto.necesita_metodologia():
        messages.error(
            request,
            f'El proyecto "{proyecto.nombre}" aún no tiene metodología asignada. '
            'El líder debe asignar una metodología antes de crear requerimientos.'
        )
        return redirect('dashboards:lider_dashboard')
    
    # Validación 2: Verificar permisos (líder o developer del proyecto)
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    
    if not (es_lider or es_participante):
        messages.error(
            request,
            'No tienes permiso para crear requerimientos en este proyecto. '
            'Solo el líder y los participantes pueden hacerlo.'
        )
        return redirect('dashboards:lider_dashboard')
    
    # Determinar qué formulario usar según la metodología
    es_tradicional = proyecto.metodologia == 'TRADICIONAL'
    es_agil = proyecto.metodologia == 'AGIL'
    
    if request.method == 'POST':
        # Instanciar el formulario apropiado
        if es_tradicional:
            form = RequerimientoTradicionalForm(request.POST)
        elif es_agil:
            form = RequerimientoAgilForm(request.POST)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('dashboards:lider_dashboard')
        
        if form.is_valid():
            # Crear el requerimiento base
            requerimiento = Requerimiento(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                tipo=form.cleaned_data['tipo'],
                estado=form.cleaned_data['estado'],
                proyecto=proyecto,
                creado_por=request.user
            )
            requerimiento.save()
            
            # Crear el detalle específico según la metodología
            if es_tradicional:
                # Crear detalle tradicional (la relación se establece automáticamente vía requerimiento_padre)
                DetalleRequerimientoTradicional.objects.create(
                    requerimiento_padre=requerimiento,
                    prioridad=form.cleaned_data.get('prioridad', ''),
                    fuente=form.cleaned_data.get('fuente', ''),
                    categoria=form.cleaned_data.get('categoria', ''),
                    fecha_compromiso=form.cleaned_data.get('fecha_compromiso'),
                    estado_validacion=form.cleaned_data.get('estado_validacion', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                messages.success(request, f'✅ Requerimiento "{requerimiento.nombre}" creado exitosamente.')
                
            elif es_agil:
                # Crear detalle ágil (la relación se establece automáticamente vía requerimiento_padre)
                DetalleRequerimientoAgil.objects.create(
                    requerimiento_padre=requerimiento,
                    historia_usuario=form.cleaned_data.get('historia_usuario', ''),
                    criterio_aceptacion=form.cleaned_data.get('criterio_aceptacion', ''),
                    puntos_estimados=form.cleaned_data.get('puntos_estimados'),
                    sprint_asignado=form.cleaned_data.get('sprint_asignado', ''),
                    responsable=form.cleaned_data.get('responsable', ''),
                    estado_scrum=form.cleaned_data.get('estado_scrum', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                messages.success(request, f'✅ User Story "{requerimiento.nombre}" creada exitosamente.')
            
            # Redirigir al dashboard del líder
            return redirect('dashboards:lider_dashboard')
    else:
        # GET: Instanciar formulario vacío
        if es_tradicional:
            form = RequerimientoTradicionalForm()
        elif es_agil:
            form = RequerimientoAgilForm()
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('dashboards:lider_dashboard')
    
    # Determinar título de página
    if es_agil:
        page_title = f"Crear User Story - {proyecto.nombre}"
    else:
        page_title = f"Crear Requerimiento - {proyecto.nombre}"
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'es_tradicional': es_tradicional,
        'es_agil': es_agil,
        'metodologia_display': proyecto.get_metodologia_display(),
        'page_title': page_title
    }
    
    return render(request, 'requerimientos/requerimiento_create.html', context)

@login_required
def requerimiento_priorizar(request, proyecto_id=None):
    from requerimientos.models import Requerimiento, DetalleRequerimientoTradicional
    from proyectos.models import Proyecto
    MOSCOW_CHOICES = [
        ("MUST", "Must have"),
        ("SHOULD", "Should have"),
        ("COULD", "Could have"),
        ("WONT", "Won't have")
    ]

    # Determinar el proyecto
    if not proyecto_id:
        proyecto_id = request.GET.get('proyecto_id')
    if not proyecto_id and hasattr(request.user, 'lidera_proyectos'):
        proyectos_liderados = request.user.lidera_proyectos.all()
        if proyectos_liderados.exists():
            proyecto_id = proyectos_liderados.first().pk
    if not proyecto_id:
        return render(request, "requerimientos/requerimiento_priorizar.html", {"proyecto": None})
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.user != proyecto.lider:
        return render(request, "requerimientos/requerimiento_priorizar.html", {"proyecto": None})

    requerimientos = Requerimiento.objects.filter(proyecto=proyecto).select_related('detalle_tradicional')

    if request.method == 'POST':
        for req in requerimientos:
            prioridad = request.POST.get(f'prioridad_{req.pk}')
            if req.detalle_tradicional:
                if prioridad and req.detalle_tradicional.prioridad != prioridad:
                    req.detalle_tradicional.prioridad = prioridad
                    req.detalle_tradicional.save()
        return redirect(f"{reverse('requerimientos:requerimiento_priorizar')}?proyecto_id={proyecto.pk}")

    context = {
        "proyecto": proyecto,
        "requerimientos": requerimientos,
        "MOSCOW_CHOICES": MOSCOW_CHOICES,
    }
    return render(request, "requerimientos/requerimiento_priorizar.html", context)


@login_required
def buscar_requerimientos_ajax(request):
    """Endpoint AJAX para búsqueda de requerimientos"""
    search_query = request.GET.get('q', '').strip()
    proyecto_id = request.GET.get('proyecto_id', '').strip()
    estado = request.GET.get('estado', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    
    # Construir filtros
    filtros = Q()
    
    if search_query:
        filtros &= (
            Q(nombre__icontains=search_query) | 
            Q(descripcion__icontains=search_query)
        )
    
    if proyecto_id:
        filtros &= Q(proyecto_id=proyecto_id)
    
    if estado:
        filtros &= Q(estado=estado)
    
    if tipo:
        filtros &= Q(tipo=tipo)
    
    # Si no hay filtros, devolver vacío
    if not (search_query or proyecto_id or estado or tipo):
        return JsonResponse({'requerimientos': [], 'count': 0})
    
    # Buscar requerimientos con prefetch_related para optimizar
    requerimientos = Requerimiento.objects.filter(filtros).select_related(
        'proyecto', 'creado_por'
    ).prefetch_related('casos_relacionados').order_by('-fecha_creacion')[:100]
    
    # Serializar requerimientos
    requerimientos_data = []
    for req in requerimientos:
        # Truncar descripción
        descripcion = req.descripcion if req.descripcion else ''
        if len(descripcion) > 60:
            descripcion = descripcion[:57] + '...'
        
        # Obtener casos relacionados
        casos = []
        for caso in req.casos_relacionados.all():
            casos.append({
                'id': caso.pk,
                'nombre': caso.nombre
            })
        
        requerimientos_data.append({
            'id': req.pk,
            'nombre': req.nombre,
            'tipo': req.tipo,
            'tipo_display': req.get_tipo_display(),  # type: ignore[attr-defined]
            'estado': req.estado,
            'estado_display': req.get_estado_display(),  # type: ignore[attr-defined]
            'descripcion': descripcion,
            'fecha_creacion': req.fecha_creacion.strftime('%d/%m/%Y'),
            'casos': casos
        })
    
    return JsonResponse({
        'requerimientos': requerimientos_data,
        'count': len(requerimientos_data)
    })
