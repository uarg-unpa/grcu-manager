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
            primer_proyecto = proyectos_liderados.first()
            if primer_proyecto:
                proyecto_id = primer_proyecto.pk

    # Si es un developer y no se especifica proyecto, usar sus proyectos
    if not proyecto_id and request.user.es_desarrollador():
        proyectos_participa = Proyecto.objects.filter(participantes=request.user)
        if proyectos_participa.exists():
            primer_proyecto = proyectos_participa.first()
            if primer_proyecto:
                proyecto_id = primer_proyecto.pk

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
            form = RequerimientoTradicionalForm(request.POST, request.FILES)
        elif es_agil:
            form = RequerimientoAgilForm(request.POST, request.FILES)
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
                creado_por=request.user,
                imagen=form.cleaned_data.get('imagen'),
                link_externo=form.cleaned_data.get('link_externo', '')
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
        page_title = f"{proyecto.nombre} - Crear User Story"
    else:
        page_title = f"{proyecto.nombre} - Crear Requerimiento"
    
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
            primer_proyecto = proyectos_liderados.first()
            if primer_proyecto:
                proyecto_id = primer_proyecto.pk
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
        "page_title": f"{proyecto.nombre} - Priorización de Requerimientos",
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


# ============================================================================
# VISTAS DE HISTORIAL (django-simple-history)
# ============================================================================

@login_required
def requerimiento_historial(request, pk):
    """
    Muestra el historial completo de versiones de un requerimiento.
    Solo usuarios con acceso al proyecto pueden ver el historial.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar permisos: solo líderes o participantes del proyecto
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(pk=request.user.pk).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para ver el historial de este requerimiento.")
        return redirect('proyectos:lista_proyectos')
    
    # Obtener historial ordenado por fecha (más reciente primero)
    historial = requerimiento.history.all().order_by('-history_date')  # type: ignore[attr-defined]
    
    # Preparar datos de versiones con información del cambio
    versiones = []
    for idx, version in enumerate(historial):
        # Calcular número de versión (más reciente = 1)
        numero_version = len(historial) - idx
        
        # Información del usuario que hizo el cambio
        usuario = version.history_user if version.history_user else None
        
        # Tipo de cambio
        tipo_cambio = {
            '+': 'Creación',
            '~': 'Modificación',
            '-': 'Eliminación'
        }.get(version.history_type, 'Desconocido')
        
        versiones.append({
            'version': version,
            'numero': numero_version,
            'usuario': usuario,
            'tipo_cambio': tipo_cambio,
            'history_id': version.history_id,
        })
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'versiones': versiones,
        'total_versiones': len(versiones),
        'page_title': f'{proyecto.nombre} - Historial de {requerimiento.nombre}',
    }
    
    return render(request, 'requerimientos/historial.html', context)


@login_required
def requerimiento_version_detail(request, pk, history_id):
    """
    Muestra los detalles de una versión específica del requerimiento.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar permisos
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(pk=request.user.pk).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para ver esta información.")
        return redirect('proyectos:lista_proyectos')
    
    # Obtener la versión histórica específica
    version = get_object_or_404(
        requerimiento.history.model,  # type: ignore[attr-defined]
        history_id=history_id,
        id=pk
    )
    
    # Calcular número de versión
    historial_completo = requerimiento.history.all().order_by('-history_date')  # type: ignore[attr-defined]
    numero_version = None
    for idx, v in enumerate(historial_completo):
        if v.history_id == history_id:
            numero_version = len(historial_completo) - idx
            break
    
    # Tipo de cambio
    tipo_cambio = {
        '+': 'Creación',
        '~': 'Modificación',
        '-': 'Eliminación'
    }.get(version.history_type, 'Desconocido')
    
    # Obtener versión anterior para comparar
    version_anterior = version.prev_record
    cambios = []
    
    if version_anterior:
        # Comparar campos importantes
        campos = [
            ('nombre', 'Nombre'),
            ('descripcion', 'Descripción'),
            ('tipo', 'Tipo'),
            ('estado', 'Estado'),
            ('prioridad', 'Prioridad'),
        ]
        
        for campo, etiqueta in campos:
            valor_actual = getattr(version, campo, '')
            valor_anterior = getattr(version_anterior, campo, '')
            
            if valor_actual != valor_anterior:
                cambios.append({
                    'campo': etiqueta,
                    'anterior': valor_anterior,
                    'actual': valor_actual,
                })
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'version': version,
        'numero_version': numero_version,
        'tipo_cambio': tipo_cambio,
        'cambios': cambios,
        'version_anterior': version_anterior,
        'page_title': f'{proyecto.nombre} - Versión #{numero_version} de {requerimiento.nombre}',
    }
    
    return render(request, 'requerimientos/version_detail.html', context)


@login_required
def requerimiento_comparar_versiones(request, pk):
    """
    Compara dos versiones específicas del requerimiento.
    Recibe version1_id y version2_id por GET.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar permisos
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(pk=request.user.pk).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para comparar versiones.")
        return redirect('proyectos:lista_proyectos')
    
    # Obtener IDs de versiones a comparar
    history_id_1 = request.GET.get('version1_id')
    history_id_2 = request.GET.get('version2_id')
    
    if not history_id_1 or not history_id_2:
        messages.error(request, "Debes seleccionar dos versiones para comparar.")
        return redirect('requerimientos:requerimiento_historial', pk=pk)
    
    # Obtener versiones
    try:
        version1 = requerimiento.history.get(history_id=history_id_1)  # type: ignore[attr-defined]
        version2 = requerimiento.history.get(history_id=history_id_2)  # type: ignore[attr-defined]
    except:
        messages.error(request, "Una o ambas versiones no existen.")
        return redirect('requerimientos:requerimiento_historial', pk=pk)
    
    # Asegurar que version1 es la más antigua
    if version1.history_date > version2.history_date:
        version1, version2 = version2, version1
    
    # Calcular números de versión
    historial_completo = requerimiento.history.all().order_by('-history_date')  # type: ignore[attr-defined]
    numero_v1 = None
    numero_v2 = None
    
    for idx, v in enumerate(historial_completo):
        if v.history_id == version1.history_id:
            numero_v1 = len(historial_completo) - idx
        if v.history_id == version2.history_id:
            numero_v2 = len(historial_completo) - idx
    
    # Comparar todos los campos importantes
    campos = [
        ('nombre', 'Nombre'),
        ('descripcion', 'Descripción'),
        ('tipo', 'Tipo'),
        ('estado', 'Estado'),
        ('prioridad', 'Prioridad'),
    ]
    
    diferencias = []
    for campo, etiqueta in campos:
        valor_v1 = getattr(version1, campo, '')
        valor_v2 = getattr(version2, campo, '')
        
        if valor_v1 != valor_v2:
            diferencias.append({
                'campo': etiqueta,
                'version1': valor_v1,
                'version2': valor_v2,
                'cambio': True,
            })
        else:
            diferencias.append({
                'campo': etiqueta,
                'version1': valor_v1,
                'version2': valor_v2,
                'cambio': False,
            })
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'version1': version1,
        'version2': version2,
        'numero_v1': numero_v1,
        'numero_v2': numero_v2,
        'diferencias': diferencias,
        'page_title': f'{proyecto.nombre} - Comparar versiones de {requerimiento.nombre}',
    }
    
    return render(request, 'requerimientos/comparar_versiones.html', context)


@login_required
def relacionar_casos_existentes(request, pk):
    """
    Vista para mostrar casos de uso existentes del proyecto y permitir relacionarlos con un requerimiento.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto

    # Verificar permisos: solo líderes o participantes del proyecto
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()

    if not (es_lider or es_participante):
        messages.error(
            request,
            'No tienes permiso para relacionar casos de uso con este requerimiento.'
        )
        return redirect('requerimientos:requerimiento_detail', pk=pk)

    if request.method == 'POST':
        # Procesar la selección de casos de uso
        casos_seleccionados = request.POST.getlist('casos_seleccionados')

        if not casos_seleccionados:
            messages.warning(request, 'No se seleccionaron casos de uso para relacionar.')
            return redirect('requerimientos:relacionar_casos_existentes', pk=pk)

        from casos_de_uso.models import CasoDeUso
        from requerimientos.models import RequerimientoCaso

        casos_relacionados = 0
        casos_ya_relacionados = 0

        for caso_id in casos_seleccionados:
            try:
                caso = CasoDeUso.objects.get(pk=caso_id, proyecto=proyecto)

                # Verificar si ya están relacionados
                relacion_existente = RequerimientoCaso.objects.filter(
                    requerimiento=requerimiento,
                    caso_de_uso=caso
                ).exists()

                if not relacion_existente:
                    RequerimientoCaso.objects.create(
                        requerimiento=requerimiento,
                        caso_de_uso=caso
                    )
                    casos_relacionados += 1
                else:
                    casos_ya_relacionados += 1

            except CasoDeUso.DoesNotExist:
                continue

        if casos_relacionados > 0:
            messages.success(
                request,
                f'✅ Se relacionaron {casos_relacionados} caso(s) de uso con el requerimiento "{requerimiento.nombre}".'
            )

        if casos_ya_relacionados > 0:
            messages.info(
                request,
                f'ℹ️ {casos_ya_relacionados} caso(s) de uso ya estaban relacionados.'
            )

        return redirect('requerimientos:requerimiento_detail', pk=pk)

    # GET: Mostrar casos de uso disponibles
    from casos_de_uso.models import CasoDeUso

    # Obtener todos los casos de uso del proyecto
    casos_disponibles = CasoDeUso.objects.filter(proyecto=proyecto).select_related('proyecto')

    # Obtener casos ya relacionados con este requerimiento
    casos_relacionados_ids = requerimiento.casos_relacionados.values_list('id', flat=True)

    # Filtrar casos que no están relacionados aún
    casos_no_relacionados = casos_disponibles.exclude(id__in=casos_relacionados_ids)

    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'casos_no_relacionados': casos_no_relacionados,
        'casos_relacionados': requerimiento.casos_relacionados.all(),
        'page_title': f'{proyecto.nombre} - Relacionar Casos de Uso con {requerimiento.nombre}',
    }

    return render(request, 'requerimientos/relacionar_casos_existentes.html', context)


@login_required
def requerimiento_update(request, pk):
    """
    Vista para editar un requerimiento existente.
    Solo el líder del proyecto o el creador pueden editar.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Validar permisos
    es_lider = request.user == proyecto.lider
    es_creador = request.user == requerimiento.creado_por
    
    if not (es_lider or es_creador):
        messages.error(request, 'No tienes permiso para editar este requerimiento.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    # Determinar qué formulario usar según la metodología
    es_tradicional = proyecto.metodologia == 'TRADICIONAL'
    es_agil = proyecto.metodologia == 'AGIL'
    
    if request.method == 'POST':
        if es_tradicional:
            form = RequerimientoTradicionalForm(request.POST, request.FILES, instance=requerimiento)
        elif es_agil:
            form = RequerimientoAgilForm(request.POST, request.FILES, instance=requerimiento)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
        
        if form.is_valid():
            # Actualizar requerimiento base
            requerimiento.nombre = form.cleaned_data['nombre']
            requerimiento.descripcion = form.cleaned_data.get('descripcion', '')
            requerimiento.tipo = form.cleaned_data['tipo']
            requerimiento.estado = form.cleaned_data['estado']
            requerimiento.imagen = form.cleaned_data.get('imagen')
            requerimiento.link_externo = form.cleaned_data.get('link_externo', '')
            requerimiento.save()
            
            # Actualizar el detalle específico según la metodología
            if es_tradicional:
                detalle, created = DetalleRequerimientoTradicional.objects.get_or_create(
                    requerimiento_padre=requerimiento
                )
                detalle.prioridad = form.cleaned_data.get('prioridad', '')
                detalle.fuente = form.cleaned_data.get('fuente', '')
                detalle.categoria = form.cleaned_data.get('categoria', '')
                detalle.fecha_compromiso = form.cleaned_data.get('fecha_compromiso')
                detalle.estado_validacion = form.cleaned_data.get('estado_validacion', '')
                detalle.observaciones = form.cleaned_data.get('observaciones', '')
                detalle.save()
                
            elif es_agil:
                detalle, created = DetalleRequerimientoAgil.objects.get_or_create(
                    requerimiento_padre=requerimiento
                )
                detalle.historia_usuario = form.cleaned_data.get('historia_usuario', '')
                detalle.criterio_aceptacion = form.cleaned_data.get('criterio_aceptacion', '')
                detalle.puntos_estimados = form.cleaned_data.get('puntos_estimados')
                detalle.sprint_asignado = form.cleaned_data.get('sprint_asignado', '')
                detalle.responsable = form.cleaned_data.get('responsable', '')
                detalle.estado_scrum = form.cleaned_data.get('estado_scrum', '')
                detalle.observaciones = form.cleaned_data.get('observaciones', '')
                detalle.save()
            
            messages.success(request, f'✅ Requerimiento "{requerimiento.nombre}" actualizado exitosamente.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
    else:
        # GET: Cargar datos existentes en el formulario
        initial_data = {
            'nombre': requerimiento.nombre,
            'descripcion': requerimiento.descripcion,
            'tipo': requerimiento.tipo,
            'estado': requerimiento.estado,
            'imagen': requerimiento.imagen,
            'link_externo': requerimiento.link_externo,
        }
        
        # Agregar datos del detalle si existe
        if es_tradicional:
            try:
                detalle = requerimiento.detalle_tradicional
                if detalle:
                    initial_data.update({
                        'prioridad': detalle.prioridad,
                        'fuente': detalle.fuente,
                        'categoria': detalle.categoria,
                        'fecha_compromiso': detalle.fecha_compromiso,
                        'estado_validacion': detalle.estado_validacion,
                        'observaciones': detalle.observaciones,
                    })
            except DetalleRequerimientoTradicional.DoesNotExist:
                pass
            form = RequerimientoTradicionalForm(initial=initial_data)
        elif es_agil:
            try:
                detalle = requerimiento.detalle_agil
                if detalle:
                    initial_data.update({
                        'historia_usuario': detalle.historia_usuario,
                        'criterio_aceptacion': detalle.criterio_aceptacion,
                        'puntos_estimados': detalle.puntos_estimados,
                        'sprint_asignado': detalle.sprint_asignado,
                        'responsable': detalle.responsable,
                        'estado_scrum': detalle.estado_scrum,
                        'observaciones': detalle.observaciones,
                    })
            except DetalleRequerimientoAgil.DoesNotExist:
                pass
            form = RequerimientoAgilForm(initial=initial_data)
        else:
            messages.error(request, 'No se pudo cargar el formulario de edición.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'requerimiento': requerimiento,
        'es_tradicional': es_tradicional,
        'es_agil': es_agil,
        'page_title': f'Editar Requerimiento: {requerimiento.nombre}',
    }
    return render(request, 'requerimientos/requerimiento_edit.html', context)


@login_required
def requerimiento_delete(request, pk):
    """
    Vista para eliminar un requerimiento.
    Solo el líder del proyecto puede eliminar.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Validar permisos: solo el líder puede eliminar
    if request.user != proyecto.lider:
        messages.error(request, 'Solo el líder del proyecto puede eliminar requerimientos.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    if request.method == 'POST':
        nombre = requerimiento.nombre
        proyecto_id = proyecto.id
        requerimiento.delete()
        messages.success(request, f'✅ Requerimiento "{nombre}" eliminado exitosamente.')
        return redirect('requerimientos:requerimiento_list')
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'page_title': f'Eliminar Requerimiento: {requerimiento.nombre}',
    }
    return render(request, 'requerimientos/requerimiento_confirm_delete.html', context)
