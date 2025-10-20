from django.shortcuts import render, get_object_or_404, redirect
from .models import CasoDeUso
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

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
