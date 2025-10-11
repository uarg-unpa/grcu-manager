from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Requerimiento
from proyectos.models import Proyecto
from django.contrib.auth.decorators import login_required
from .forms import RequerimientoForm
from requerimientos.models import DetalleRequerimientoTradicional, DetalleRequerimientoAgil
from django.utils import timezone
from django.http import JsonResponse

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
    proyecto = None
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = RequerimientoForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.creado_por = request.user
            req.fecha_creacion = timezone.now()
            req.save()

            # Crear detalle según metodología del proyecto
            metod = proyecto.metodologia if proyecto else None
            if metod and metod.lower().startswith('trad'):
                DetalleRequerimientoTradicional.objects.create(requerimiento_padre=req)
            elif metod and metod.lower().startswith('agil'):
                DetalleRequerimientoAgil.objects.create(requerimiento_padre=req)

            if is_ajax:
                # return extra display fields so the client can render the new item
                return JsonResponse({
                    'success': True,
                    'pk': req.pk,
                    'nombre': req.nombre,
                    'tipo': req.get_tipo_display(),
                    'estado': req.get_estado_display(),
                })
            # redirect back to list; include proyecto_id as query param if present
            if proyecto:
                return redirect(f"{reverse('requerimientos:requerimiento_list')}?proyecto_id={proyecto.pk}")
            return redirect('requerimientos:requerimiento_list')
    else:
        initial = {'proyecto': proyecto} if proyecto else {}
        form = RequerimientoForm(initial=initial)

    # If AJAX GET, return partial HTML for modal body
    if is_ajax:
        return render(request, 'requerimientos/_requerimiento_form_partial.html', {'form': form, 'proyecto': proyecto})

    return render(request, 'requerimientos/requerimiento_form.html', {'form': form, 'proyecto': proyecto})

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
