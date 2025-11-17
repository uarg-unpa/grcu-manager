from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Requerimiento
from proyectos.models import Proyecto, ParticipacionProyecto
from django.contrib.auth.decorators import login_required
from .forms import RequerimientoForm, RequerimientoTradicionalForm, RequerimientoAgilForm
from requerimientos.models import DetalleRequerimientoTradicional, DetalleRequerimientoAgil, ComentarioValidacion
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

    # Si es un stakeholder y no se especifica proyecto, usar el primer proyecto donde es cliente
    if not proyecto_id and request.user.es_stakeholder():
        proyectos_cliente = Proyecto.objects.filter(clientes=request.user)
        if proyectos_cliente.exists():
            primer_proyecto = proyectos_cliente.first()
            if primer_proyecto:
                proyecto_id = primer_proyecto.pk

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

    # Inicializar variables
    es_stakeholder = False
    
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        
        # IMPORTANTE: Verificar stakeholder PRIMERO antes de otros roles
        # Un usuario es stakeholder si tiene el rol Stakeholder Y está en la lista de clientes del proyecto
        tiene_rol_stakeholder = request.user.es_stakeholder()
        esta_en_clientes = proyecto.clientes.filter(id=request.user.id).exists()
        es_stakeholder = tiene_rol_stakeholder and esta_en_clientes
        
        # SEGURIDAD: Si el usuario SOLO es stakeholder (no líder ni participante)
        # y NO está en la lista de clientes de este proyecto, bloquear acceso
        es_lider = request.user == proyecto.lider
        es_participante = proyecto.participantes.filter(id=request.user.id).exists()
        
        if tiene_rol_stakeholder and not (es_lider or es_participante or esta_en_clientes):
            # Stakeholder intentando acceder a un proyecto donde NO es cliente
            from django.contrib import messages
            messages.error(request, "No tienes permiso para ver los requerimientos de este proyecto.")
            # Redirigir a sus proyectos como cliente
            return redirect('dashboards:stakeholder_dashboard')
        
        if es_stakeholder:
            # Stakeholders solo ven requerimientos pendientes de validación (BORRADOR)
            # independientemente de si también son participantes
            requerimientos = Requerimiento.objects.filter(
                proyecto=proyecto,
                estado='BORRADOR'
            ).select_related('proyecto').prefetch_related('dependencias').annotate(
                num_comentarios=Count('comentarios_validacion', distinct=True)
            )
        else:
            # Líderes y desarrolladores ven todos los requerimientos
            requerimientos = Requerimiento.objects.filter(proyecto=proyecto).select_related(
                'proyecto', 'detalle_tradicional', 'detalle_agil'
            ).prefetch_related('dependencias').annotate(
                num_comentarios=Count('comentarios_validacion', distinct=True)
            )
        
        # Estadísticas adicionales para líderes
        stats = None
        if es_lider:
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
        requerimientos = Requerimiento.objects.all().select_related(
            'proyecto', 'detalle_tradicional', 'detalle_agil'
        ).prefetch_related('dependencias').annotate(
            num_comentarios=Count('comentarios_validacion', distinct=True)
        )
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
        "is_lider": proyecto and request.user == proyecto.lider,
        "is_stakeholder": es_stakeholder,
        "page_title": page_title,
        # Agregar conteo de requerimientos pendientes de validación
        "pendientes_validacion": Requerimiento.objects.filter(proyecto=proyecto, estado='BORRADOR').count() if proyecto else 0,
        "MOSCOW_CHOICES": [
            ("MUST", "Crítico"),
            ("SHOULD", "Importante"),
            ("COULD", "Deseable"),
            ("WONT", "Descartado")
        ],
    }
    return render(request, "requerimientos/requerimiento_list.html", context)

@login_required
def requerimiento_detail(request, pk):
    """
    Vista de detalle del requerimiento que muestra información completa
    incluyendo comentarios y conversaciones de validación.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar permisos: participantes del proyecto y clientes pueden ver detalles
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    es_cliente = request.user.es_stakeholder() and proyecto.clientes.filter(id=request.user.id).exists()
    tiene_permiso = es_lider or es_participante or es_cliente
    
    # Obtener comentarios si el usuario tiene permiso
    comentarios = []
    comentarios_hilo = []
    
    if tiene_permiso:
        # Obtener comentarios ordenados por fecha con información completa del autor
        comentarios = ComentarioValidacion.objects.filter(
            requerimiento=requerimiento
        ).select_related('autor', 'comentario_padre').order_by('fecha_creacion')
        
        # Organizar comentarios en hilos
        comentarios_raiz = comentarios.filter(comentario_padre__isnull=True)
        
        for comentario in comentarios_raiz:
            hilo = {
                'comentario': comentario,
                'respuestas': list(comentarios.filter(comentario_padre=comentario))
            }
            comentarios_hilo.append(hilo)
    
    context = {
        'requerimiento': requerimiento,
        'comentarios_hilo': comentarios_hilo,
        'total_comentarios': len(comentarios),
        'tiene_permiso': tiene_permiso,
        'es_lider': es_lider,
        'es_participante': es_participante,
        'es_cliente': es_cliente,
        'is_stakeholder': es_cliente,  # Alias para mantener consistencia con template
    }
    
    return render(request, "requerimientos/requerimiento_detail.html", context)


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
        # Instanciar el formulario apropiado con datos POST y archivos
        if es_tradicional:
            form = RequerimientoTradicionalForm(request.POST, request.FILES, proyecto=proyecto)
        elif es_agil:
            form = RequerimientoAgilForm(request.POST, request.FILES)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('dashboards:lider_dashboard')
        
        if form.is_valid():
            # Combinar identificador y nombre
            identificador = form.cleaned_data.get('identificador', '').strip()
            nombre = form.cleaned_data.get('nombre', '').strip()
            nombre_completo = f"{identificador} - {nombre}" if identificador else nombre
            
            # Crear el requerimiento base
            requerimiento = Requerimiento(
                nombre=nombre_completo,
                descripcion=form.cleaned_data.get('descripcion', ''),
                tipo=form.cleaned_data['tipo'],
                estado='BORRADOR',  # Forzar estado inicial como BORRADOR
                proyecto=proyecto,
                creado_por=request.user,
                imagen=form.cleaned_data.get('imagen'),
                link_externo=form.cleaned_data.get('link_externo', '')
            )
            requerimiento.save()
            
            # Crear el detalle específico según la metodología
            if es_tradicional:
                from .models import FuenteRequerimiento, CategoriaRequerimiento
                
                # Manejar fuente (crear nueva si es necesario)
                fuente_valor = form.cleaned_data.get('fuente', '')
                if fuente_valor == 'NUEVA':
                    nueva_fuente_nombre = form.cleaned_data.get('nueva_fuente', '').strip()
                    if nueva_fuente_nombre:
                        # Crear nueva fuente personalizada
                        fuente_obj, created = FuenteRequerimiento.objects.get_or_create(
                            proyecto=proyecto,
                            nombre=nueva_fuente_nombre,
                            defaults={'creado_por': request.user}
                        )
                        fuente_valor = nueva_fuente_nombre
                        if created:
                            messages.info(request, f'✨ Nueva fuente "{nueva_fuente_nombre}" agregada al proyecto.')
                    else:
                        fuente_valor = ''
                elif fuente_valor:
                    # Incrementar contador de uso
                    try:
                        fuente_obj = FuenteRequerimiento.objects.get(proyecto=proyecto, nombre=fuente_valor)
                        fuente_obj.incrementar_uso()
                    except FuenteRequerimiento.DoesNotExist:
                        pass
                
                # Manejar categoría (crear nueva si es necesario)
                categoria_valor = form.cleaned_data.get('categoria', '')
                if categoria_valor == 'NUEVA':
                    nueva_categoria_nombre = form.cleaned_data.get('nueva_categoria', '').strip()
                    if nueva_categoria_nombre:
                        # Crear nueva categoría personalizada
                        categoria_obj, created = CategoriaRequerimiento.objects.get_or_create(
                            proyecto=proyecto,
                            nombre=nueva_categoria_nombre,
                            defaults={'creado_por': request.user}
                        )
                        categoria_valor = nueva_categoria_nombre
                        if created:
                            messages.info(request, f'✨ Nueva categoría "{nueva_categoria_nombre}" agregada al proyecto.')
                    else:
                        categoria_valor = ''
                elif categoria_valor:
                    # Incrementar contador de uso
                    try:
                        categoria_obj = CategoriaRequerimiento.objects.get(proyecto=proyecto, nombre=categoria_valor)
                        categoria_obj.incrementar_uso()
                    except CategoriaRequerimiento.DoesNotExist:
                        pass
                
                # Crear detalle tradicional (la relación se establece automáticamente vía requerimiento_padre)
                DetalleRequerimientoTradicional.objects.create(
                    requerimiento_padre=requerimiento,
                    prioridad=form.cleaned_data.get('prioridad', ''),
                    fuente=fuente_valor,
                    categoria=categoria_valor,
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
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                messages.success(request, f'✅ User Story "{requerimiento.nombre}" creada exitosamente.')
            
            # Redirigir al listado de requerimientos del proyecto
            return redirect(f"{reverse('requerimientos:requerimiento_list')}?proyecto_id={proyecto.id}")
        else:
            # Si el formulario no es válido, se mantendrá con los datos POST
            # Los valores ingresados se conservarán para que el usuario los corrija
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        # GET: Generar identificador automático según tipo más frecuente del proyecto
        initial_data = {}
        
        # Analizar qué tipo de requerimiento es más común para sugerir el siguiente
        # Contar requerimientos por tipo en el proyecto
        from django.db.models import Count
        tipos_count = Requerimiento.objects.filter(proyecto=proyecto).values('tipo').annotate(
            count=Count('tipo')
        ).order_by('-count')
        
        # Determinar el tipo sugerido (el más común, o FUNCIONAL por defecto)
        tipo_sugerido = tipos_count[0]['tipo'] if tipos_count else 'FUNCIONAL'
        
        # Generar identificador automático basado en el tipo
        # RF-01 para FUNCIONAL, RNF-01 para NO_FUNCIONAL, RS-01 para SISTEMA
        prefijos = {
            'FUNCIONAL': 'RF',
            'NO_FUNCIONAL': 'RNF',
            'SISTEMA': 'RS'
        }
        
        # Identificador por defecto según el tipo más común
        prefijo_default = prefijos.get(tipo_sugerido, 'RF')
        count_default = Requerimiento.objects.filter(proyecto=proyecto, tipo=tipo_sugerido).count()
        initial_data['identificador'] = f'{prefijo_default}-{count_default + 1:02d}'
        initial_data['nombre'] = ''  # Campo nombre vacío para que el usuario lo complete
        
        # Instanciar formulario con datos iniciales
        if es_tradicional:
            form = RequerimientoTradicionalForm(initial=initial_data, proyecto=proyecto)
        elif es_agil:
            form = RequerimientoAgilForm(initial=initial_data)
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
        ("MUST", "Crítico"),
        ("SHOULD", "Importante"),
        ("COULD", "Deseable"),
        ("WONT", "Descartado")
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

    # Obtener requerimientos del proyecto que estén VALIDADOS (listos para priorizar)
    # Los requerimientos en estado BORRADOR no pueden priorizarse
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).exclude(
        estado='BORRADOR'
    ).select_related('detalle_tradicional', 'detalle_agil').prefetch_related('comentarios_validacion')
    
    # Agregar comentarios de validación a cada requerimiento
    from requerimientos.models import ComentarioValidacion
    requerimientos_con_comentarios = []
    for req in requerimientos:
        # Obtener el último comentario de validación (si existe)
        ultimo_comentario = ComentarioValidacion.objects.filter(
            requerimiento=req,
            tipo_accion__in=['VALIDAR', 'ACLARACION']
        ).order_by('-fecha_creacion').first()
        
        requerimientos_con_comentarios.append({
            'requerimiento': req,
            'ultimo_comentario': ultimo_comentario.comentario if ultimo_comentario else None
        })

    if request.method == 'POST':
        for item in requerimientos_con_comentarios:
            req = item['requerimiento']
            # Solo permitir priorizar requerimientos validados
            if req.estado == 'BORRADOR':
                continue
                
            prioridad = request.POST.get(f'prioridad_{req.pk}')
            if prioridad:
                detalle_actualizado = False
                
                # Intentar acceder a detalle tradicional usando hasattr
                if hasattr(req, 'detalle_tradicional'):
                    try:
                        detalle_trad = req.detalle_tradicional
                        if detalle_trad:
                            detalle_trad.prioridad = prioridad
                            detalle_trad.save()
                            detalle_actualizado = True
                    except DetalleRequerimientoTradicional.DoesNotExist:
                        pass
                
                # Intentar acceder a detalle ágil si no se actualizó tradicional
                if not detalle_actualizado and hasattr(req, 'detalle_agil'):
                    try:
                        detalle_agil = req.detalle_agil
                        if detalle_agil:
                            detalle_agil.prioridad = prioridad
                            detalle_agil.save()
                            detalle_actualizado = True
                    except DetalleRequerimientoAgil.DoesNotExist:
                        pass
                
                # Si no tiene ningún detalle, crear según metodología del proyecto
                if not detalle_actualizado:
                    if proyecto.metodologia == 'TRADICIONAL':
                        DetalleRequerimientoTradicional.objects.create(
                            requerimiento_padre=req, 
                            prioridad=prioridad
                        )
                    elif proyecto.metodologia == 'AGIL':
                        DetalleRequerimientoAgil.objects.create(
                            requerimiento_padre=req, 
                            prioridad=prioridad
                        )
                
                # Cambiar estado a PRIORIZADO si no lo está
                if req.estado != 'PRIORIZADO':
                    req.estado = 'PRIORIZADO'
                    req.save()
        
        messages.success(request, '✅ Priorización realizada con éxito. Los requerimientos han sido actualizados.')
        return redirect(f"{reverse('requerimientos:requerimiento_priorizar')}?proyecto_id={proyecto.pk}")

    context = {
        "proyecto": proyecto,
        "requerimientos": requerimientos_con_comentarios,
        "MOSCOW_CHOICES": MOSCOW_CHOICES,
        "page_title": f"{proyecto.nombre} - Priorización de Requerimientos",
    }
    return render(request, "requerimientos/requerimiento_priorizar.html", context)


@login_required
def obtener_siguiente_numero_requerimiento(request):
    """Endpoint AJAX para obtener el siguiente número de requerimiento según el tipo"""
    proyecto_id = request.GET.get('proyecto_id', '').strip()
    tipo = request.GET.get('tipo', 'FUNCIONAL').strip()
    
    if not proyecto_id:
        return JsonResponse({'error': 'Se requiere proyecto_id'}, status=400)
    
    # Definir prefijos según tipo
    prefijos = {
        'FUNCIONAL': 'RF',
        'NO_FUNCIONAL': 'RNF',
        'SISTEMA': 'RS'
    }
    
    prefijo = prefijos.get(tipo, 'RF')
    
    # Contar requerimientos del mismo tipo en el proyecto
    count = Requerimiento.objects.filter(proyecto_id=proyecto_id, tipo=tipo).count()
    siguiente_numero = count + 1
    siguiente_nombre = f'{prefijo}-{siguiente_numero:02d}'
    
    return JsonResponse({
        'siguiente_nombre': siguiente_nombre,
        'tipo': tipo,
        'prefijo': prefijo,
        'numero': siguiente_numero
    })

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
        'proyecto', 'creado_por', 'detalle_tradicional', 'detalle_agil'
    ).prefetch_related('casos_relacionados', 'dependencias').order_by('-fecha_creacion')[:100]
    
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
        
        # Obtener prioridad
        prioridad = None
        prioridad_display = None
        
        # Mapeo de prioridades
        PRIORIDAD_DISPLAY = {
            'MUST': 'Crítico',
            'SHOULD': 'Importante',
            'COULD': 'Deseable',
            'WONT': 'Descartado'
        }
        
        if hasattr(req, 'detalle_tradicional') and req.detalle_tradicional and req.detalle_tradicional.prioridad:
            prioridad = req.detalle_tradicional.prioridad
            prioridad_display = PRIORIDAD_DISPLAY.get(prioridad, prioridad)
        elif hasattr(req, 'detalle_agil') and req.detalle_agil and req.detalle_agil.prioridad:
            prioridad = req.detalle_agil.prioridad
            prioridad_display = PRIORIDAD_DISPLAY.get(prioridad, prioridad)
        
        # Obtener dependencias
        dependencias = []
        for dep in req.dependencias.all():
            dependencias.append({
                'id': dep.pk,
                'nombre': dep.nombre,
                'estado': dep.estado,
                'estado_display': dep.get_estado_display()  # type: ignore[attr-defined]
            })
        
        # Obtener número de comentarios
        num_comentarios = req.comentarios.count() if hasattr(req, 'comentarios') else 0
        
        requerimientos_data.append({
            'id': req.pk,
            'nombre': req.nombre,
            'tipo': req.tipo,
            'tipo_display': req.get_tipo_display(),  # type: ignore[attr-defined]
            'estado': req.estado,
            'estado_display': req.get_estado_display(),  # type: ignore[attr-defined]
            'descripcion': descripcion,
            'fecha_creacion': req.fecha_creacion.strftime('%d/%m/%Y'),
            'casos': casos,
            'prioridad': prioridad,
            'prioridad_display': prioridad_display,
            'dependencias': dependencias,
            'num_comentarios': num_comentarios,
            'proyecto_id': req.proyecto.pk,
            'proyecto_lider_id': req.proyecto.lider.pk,
            'creado_por_id': req.creado_por.pk if req.creado_por else None,
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
        # Manejar el caso cuando history_user es None (cambios por migraciones, scripts, etc.)
        if version.history_user:
            usuario = version.history_user
            usuario_nombre = usuario.nombre if hasattr(usuario, 'nombre') else str(usuario)
        else:
            usuario = None
            usuario_nombre = 'Sistema'
        
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
            'usuario_nombre': usuario_nombre,
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
        # Comparar campos importantes del modelo Requerimiento
        # NO incluir 'prioridad' porque no está en el modelo principal
        campos = [
            ('nombre', 'Nombre'),
            ('descripcion', 'Descripción'),
            ('tipo', 'Tipo'),
            ('estado', 'Estado'),
        ]
        
        for campo, etiqueta in campos:
            valor_actual = getattr(version, campo, '')
            valor_anterior = getattr(version_anterior, campo, '')
            
            if valor_actual != valor_anterior:
                cambios.append({
                    'campo': etiqueta,
                    'anterior': valor_anterior if valor_anterior else '(vacío)',
                    'actual': valor_actual if valor_actual else '(vacío)',
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
    
    # Comparar todos los campos importantes del modelo Requerimiento
    # NO incluir 'prioridad' porque está en los detalles, no en el modelo principal
    campos = [
        ('nombre', 'Nombre'),
        ('descripcion', 'Descripción'),
        ('tipo', 'Tipo'),
        ('estado', 'Estado'),
    ]
    
    diferencias = []
    for campo, etiqueta in campos:
        valor_v1 = getattr(version1, campo, '') or ''
        valor_v2 = getattr(version2, campo, '') or ''
        
        # Convertir a string para mejor visualización
        if hasattr(valor_v1, '__str__'):
            valor_v1 = str(valor_v1) if valor_v1 else '(vacío)'
        if hasattr(valor_v2, '__str__'):
            valor_v2 = str(valor_v2) if valor_v2 else '(vacío)'
        
        diferencias.append({
            'campo': etiqueta,
            'version1': valor_v1,
            'version2': valor_v2,
            'cambio': valor_v1 != valor_v2,
        })
    
    # Contar campos con cambios
    campos_con_cambios = sum(1 for diff in diferencias if diff['cambio'])
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'version1': version1,
        'version2': version2,
        'numero_v1': numero_v1,
        'numero_v2': numero_v2,
        'usuario_v1': version1.history_user,  # Pasar objeto completo o None
        'usuario_v2': version2.history_user,  # Pasar objeto completo o None
        'diferencias': diferencias,
        'campos_con_cambios': campos_con_cambios,
        'page_title': f'{proyecto.nombre} - Comparar versiones de {requerimiento.nombre}',
    }
    
    return render(request, 'requerimientos/comparar_versiones.html', context)


@login_required
def relacionar_casos_existentes(request, pk):
    """
    Vista para mostrar casos de uso existentes del proyecto y permitir relacionarlos con un requerimiento.
    Solo permite relacionar si el requerimiento está VALIDADO.
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

    # REGLA DE ORO: Solo requerimientos VALIDADOS pueden tener casos de uso
    if requerimiento.estado != 'VALIDADO':
        messages.error(
            request,
            f'No se pueden asignar casos de uso a un requerimiento en estado "{requerimiento.get_estado_display()}". '
            'El requerimiento debe estar VALIDADO primero.'
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
        # Instanciar el formulario apropiado con datos POST y archivos
        if es_tradicional:
            form = RequerimientoTradicionalForm(request.POST, request.FILES, proyecto=proyecto)
        elif es_agil:
            form = RequerimientoAgilForm(request.POST, request.FILES)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
        
        if form.is_valid():
            # Combinar identificador y nombre
            identificador = form.cleaned_data.get('identificador', '').strip()
            nombre = form.cleaned_data.get('nombre', '').strip()
            nombre_completo = f"{identificador} - {nombre}" if identificador else nombre
            
            # Actualizar requerimiento base
            requerimiento.nombre = nombre_completo
            requerimiento.descripcion = form.cleaned_data.get('descripcion', '')
            requerimiento.tipo = form.cleaned_data['tipo']
           
           
            nueva_imagen = form.cleaned_data.get('imagen')
            if nueva_imagen:
                requerimiento.imagen = nueva_imagen
            
            requerimiento.link_externo = form.cleaned_data.get('link_externo', '')
            requerimiento.save()
            
            # Actualizar el detalle específico según la metodología
            if es_tradicional:
                from .models import FuenteRequerimiento, CategoriaRequerimiento
                
                # Manejar fuente (crear nueva si es necesario)
                fuente_valor = form.cleaned_data.get('fuente', '')
                if fuente_valor == 'NUEVA':
                    nueva_fuente_nombre = form.cleaned_data.get('nueva_fuente', '').strip()
                    if nueva_fuente_nombre:
                        fuente_obj, created = FuenteRequerimiento.objects.get_or_create(
                            proyecto=proyecto,
                            nombre=nueva_fuente_nombre,
                            defaults={'creado_por': request.user}
                        )
                        fuente_valor = nueva_fuente_nombre
                        if created:
                            messages.info(request, f'✨ Nueva fuente "{nueva_fuente_nombre}" agregada al proyecto.')
                    else:
                        fuente_valor = ''
                elif fuente_valor:
                    try:
                        fuente_obj = FuenteRequerimiento.objects.get(proyecto=proyecto, nombre=fuente_valor)
                        fuente_obj.incrementar_uso()
                    except FuenteRequerimiento.DoesNotExist:
                        pass
                
                # Manejar categoría (crear nueva si es necesario)
                categoria_valor = form.cleaned_data.get('categoria', '')
                if categoria_valor == 'NUEVA':
                    nueva_categoria_nombre = form.cleaned_data.get('nueva_categoria', '').strip()
                    if nueva_categoria_nombre:
                        categoria_obj, created = CategoriaRequerimiento.objects.get_or_create(
                            proyecto=proyecto,
                            nombre=nueva_categoria_nombre,
                            defaults={'creado_por': request.user}
                        )
                        categoria_valor = nueva_categoria_nombre
                        if created:
                            messages.info(request, f'✨ Nueva categoría "{nueva_categoria_nombre}" agregada al proyecto.')
                    else:
                        categoria_valor = ''
                elif categoria_valor:
                    try:
                        categoria_obj = CategoriaRequerimiento.objects.get(proyecto=proyecto, nombre=categoria_valor)
                        categoria_obj.incrementar_uso()
                    except CategoriaRequerimiento.DoesNotExist:
                        pass
                
                detalle, created = DetalleRequerimientoTradicional.objects.get_or_create(
                    requerimiento_padre=requerimiento
                )
                # NO actualizar prioridad ni estado_validacion - se manejan en vistas específicas
                detalle.fuente = fuente_valor
                detalle.categoria = categoria_valor
                detalle.fecha_compromiso = form.cleaned_data.get('fecha_compromiso')
                detalle.observaciones = form.cleaned_data.get('observaciones', '')
                detalle.save()
                
            elif es_agil:
                detalle, created = DetalleRequerimientoAgil.objects.get_or_create(
                    requerimiento_padre=requerimiento
                )
                detalle.historia_usuario = form.cleaned_data.get('historia_usuario', '')
                detalle.criterio_aceptacion = form.cleaned_data.get('criterio_aceptacion', '')
                detalle.puntos_estimados = form.cleaned_data.get('puntos_estimados')
                detalle.observaciones = form.cleaned_data.get('observaciones', '')
                detalle.save()
            
            messages.success(request, f'✅ Requerimiento "{requerimiento.nombre}" actualizado exitosamente.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
        else:
            # Si el formulario no es válido, se mantendrá con los datos POST
            # Agregar mensaje de error
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        # GET: Cargar datos existentes en el formulario
        from typing import Any, Dict
        
        # Separar identificador y nombre si existe el formato "ID - Nombre"
        nombre_completo = requerimiento.nombre
        identificador = ''
        nombre = nombre_completo
        
        # Intentar extraer identificador si tiene formato "RF-## - Nombre"
        import re
        match = re.match(r'^(R[FNS]+F?-\d+)\s*-\s*(.+)$', nombre_completo)
        if match:
            identificador = match.group(1)
            nombre = match.group(2)
        
        initial_data: Dict[str, Any] = {
            'identificador': identificador,
            'nombre': nombre,
            'descripcion': requerimiento.descripcion,
            'tipo': requerimiento.tipo,
            # NO incluir estado - no se edita aquí
            'link_externo': requerimiento.link_externo,
        }
        
        # Agregar datos del detalle si existe
        if es_tradicional:
            try:
                detalle = requerimiento.detalle_tradicional
                if detalle:
                    initial_data.update({
                        # NO incluir prioridad ni estado_validacion
                        'fuente': detalle.fuente if detalle.fuente else '',
                        'categoria': detalle.categoria if detalle.categoria else '',
                        'fecha_compromiso': detalle.fecha_compromiso,
                        'observaciones': detalle.observaciones,
                    })
            except DetalleRequerimientoTradicional.DoesNotExist:
                pass
            form = RequerimientoTradicionalForm(initial=initial_data, proyecto=proyecto)
        elif es_agil:
            try:
                detalle = requerimiento.detalle_agil
                if detalle:
                    initial_data.update({
                        'historia_usuario': detalle.historia_usuario,
                        'criterio_aceptacion': detalle.criterio_aceptacion,
                        'puntos_estimados': detalle.puntos_estimados,
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
        'imagen_existente': requerimiento.imagen,  # Para mostrar la imagen actual
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
        proyecto_id = proyecto.pk
        requerimiento.delete()
        messages.success(request, f'✅ Requerimiento "{nombre}" eliminado exitosamente.')
        return redirect('requerimientos:requerimiento_list')
    
    context = {
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'page_title': f'Eliminar Requerimiento: {requerimiento.nombre}',
    }
    return render(request, 'requerimientos/requerimiento_confirm_delete.html', context)


# ============================================================================
# VISTAS DE VALIDACIÓN
# ============================================================================

@login_required
def requerimiento_validar_cliente(request, proyecto_id=None):
    """
    Vista para que clientes/stakeholders validen requerimientos.
    Solo muestra requerimientos en estado 'BORRADOR' que necesitan validación.
    """
    # Determinar el proyecto
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    else:
        proyecto_id = request.GET.get('proyecto_id')
        if not proyecto_id:
            messages.error(request, 'Debe especificar un proyecto para validar requerimientos.')
            return redirect('dashboards:cliente_dashboard')
        else:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificar que el usuario sea stakeholder del proyecto
    from proyectos.models import ParticipacionProyecto
    from roles.models import Rol
    try:
        stakeholder_rol = Rol.objects.get(nombre='Stakeholder')
        es_stakeholder = ParticipacionProyecto.objects.filter(
            usuario=request.user,
            proyecto=proyecto,
            rol=stakeholder_rol
        ).exists()
    except Rol.DoesNotExist:
        es_stakeholder = False
    
    if not es_stakeholder:
        messages.error(request, 'No tienes permiso para validar requerimientos de este proyecto.')
        return redirect('dashboards:cliente_dashboard')

    # Obtener requerimientos pendientes de validación (estado BORRADOR)
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto,
        estado='BORRADOR'
    ).select_related('detalle_tradicional', 'detalle_agil', 'creado_por')

    if request.method == 'POST':
        # Procesar validaciones
        for req in requerimientos:
            accion = request.POST.get(f'accion_{req.pk}')
            comentario = request.POST.get(f'comentario_{req.pk}', '')
            if accion == 'validar':
                # Validar el requerimiento
                req.estado = 'VALIDADO'
                req.validado_por = request.user
                req.fecha_validacion = timezone.now()
                req.tipo_validador = 'CLIENTE'
                req.save()
                messages.success(request, f'✅ Requerimiento "{req.nombre}" validado exitosamente.')
            elif accion == 'rechazar':
                # Rechazar el requerimiento (volver a estado BORRADOR para revisión)
                req.estado = 'BORRADOR'
                req.requiere_discusion = True
                req.motivo_rechazo = comentario if comentario else 'Rechazado sin comentario específico'
                req.ultimo_rechazado_por = request.user
                req.fecha_ultimo_rechazo = timezone.now()
                req.save()
                
                # Crear comentario de rechazo
                ComentarioValidacion.objects.create(
                    requerimiento=req,
                    autor=request.user,
                    comentario=comentario if comentario else 'Requerimiento rechazado para revisión',
                    tipo_accion='RECHAZAR'
                )
                
                messages.info(request, f'ℹ️ Requerimiento "{req.nombre}" rechazado para revisión.')

        return redirect(f"{reverse('requerimientos:requerimiento_validar_cliente_proyecto', args=[proyecto.pk])}")

    context = {
        'proyecto': proyecto,
        'requerimientos': requerimientos,
        'page_title': f'{proyecto.nombre} - Validación de Requerimientos',
    }
    return render(request, 'requerimientos/requerimiento_validar_cliente.html', context)


@login_required
def requerimiento_validar_lider(request, proyecto_id=None):
    """
    Vista para que líderes validen requerimientos.
    Solo muestra requerimientos en estado 'BORRADOR' que necesitan validación.
    """
    # Determinar el proyecto
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    else:
        proyecto_id = request.GET.get('proyecto_id')
        if not proyecto_id:
            # Si no se especifica proyecto, tomar el primer proyecto del líder
            proyecto = Proyecto.objects.filter(lider=request.user).first()
            if not proyecto:
                messages.error(request, 'No tienes proyectos asignados como líder.')
                return redirect('dashboards:lider_dashboard')
        else:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificar que el usuario sea líder del proyecto
    if request.user != proyecto.lider:
        messages.error(request, 'Solo el líder del proyecto puede validar requerimientos.')
        return redirect('dashboards:lider_dashboard')

    # Obtener requerimientos pendientes de validación (estado BORRADOR)
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto,
        estado='BORRADOR'
    ).select_related('detalle_tradicional', 'detalle_agil', 'creado_por')

    if request.method == 'POST':
        # Procesar validaciones
        for req in requerimientos:
            accion = request.POST.get(f'accion_{req.pk}')
            comentario = request.POST.get(f'comentario_{req.pk}', '').strip()
            
            if accion == 'validar':
                # Validar el requerimiento
                req.estado = 'VALIDADO'
                req.validado_por = request.user
                req.fecha_validacion = timezone.now()
                req.tipo_validador = 'LIDER'
                req.requiere_discusion = False
                req.save()
                
                # Crear comentario si se proporcionó
                if comentario:
                    ComentarioValidacion.objects.create(
                        requerimiento=req,
                        autor=request.user,
                        comentario=comentario,
                        tipo_accion='VALIDAR'
                    )
                
                messages.success(request, f'✅ Requerimiento "{req.nombre}" validado exitosamente.')
                
            elif accion == 'rechazar':
                # Rechazar el requerimiento (volver a estado BORRADOR para edición)
                req.estado = 'BORRADOR'
                req.requiere_discusion = True
                req.motivo_rechazo = comentario if comentario else 'Rechazado sin comentario específico'
                req.ultimo_rechazado_por = request.user
                req.fecha_ultimo_rechazo = timezone.now()
                req.save()
                
                # Crear comentario de rechazo
                ComentarioValidacion.objects.create(
                    requerimiento=req,
                    autor=request.user,
                    comentario=comentario if comentario else 'Requerimiento rechazado para revisión',
                    tipo_accion='RECHAZAR'
                )
                
                messages.info(request, f'ℹ️ Requerimiento "{req.nombre}" rechazado para revisión.')

        return redirect(f"{reverse('requerimientos:requerimiento_validar_lider_proyecto', args=[proyecto.pk])}")

    context = {
        'proyecto': proyecto,
        'requerimientos': requerimientos,
        'page_title': f'{proyecto.nombre} - Validación de Requerimientos',
    }
    return render(request, 'requerimientos/requerimiento_validar_lider.html', context)


@login_required
def requerimiento_validar_lider_individual(request, pk):
    """
    Vista para que el líder valide un requerimiento específico.
    Muestra solo el requerimiento solicitado.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar que el usuario sea líder del proyecto
    if request.user != proyecto.lider:
        messages.error(request, 'Solo el líder del proyecto puede validar requerimientos.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    # Verificar que el requerimiento esté en estado BORRADOR
    if requerimiento.estado != 'BORRADOR':
        messages.info(request, f'Este requerimiento ya fue {requerimiento.get_estado_display().lower()}.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        comentario = request.POST.get('comentario', '').strip()
        
        if accion == 'validar':
            # Validar el requerimiento
            requerimiento.estado = 'VALIDADO'
            requerimiento.validado_por = request.user
            requerimiento.fecha_validacion = timezone.now()
            requerimiento.tipo_validador = 'LIDER'
            requerimiento.requiere_discusion = False
            requerimiento.save()
            
            # Crear comentario si se proporcionó
            if comentario:
                ComentarioValidacion.objects.create(
                    requerimiento=requerimiento,
                    autor=request.user,
                    comentario=comentario,
                    tipo_accion='VALIDAR'
                )
            
            messages.success(request, f'✅ Requerimiento "{requerimiento.nombre}" validado exitosamente.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
            
        elif accion == 'rechazar':
            if not comentario:
                messages.error(request, 'Debes proporcionar un comentario al rechazar un requerimiento.')
            else:
                # Rechazar el requerimiento
                requerimiento.estado = 'BORRADOR'
                requerimiento.requiere_discusion = True
                requerimiento.motivo_rechazo = comentario
                requerimiento.ultimo_rechazado_por = request.user
                requerimiento.fecha_ultimo_rechazo = timezone.now()
                requerimiento.save()
                
                # Crear comentario de rechazo
                ComentarioValidacion.objects.create(
                    requerimiento=requerimiento,
                    autor=request.user,
                    comentario=comentario,
                    tipo_accion='RECHAZAR'
                )
                
                messages.info(request, f'ℹ️ Requerimiento "{requerimiento.nombre}" rechazado para revisión.')
                return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    context = {
        'proyecto': proyecto,
        'requerimiento': requerimiento,
        'page_title': f'Validar: {requerimiento.nombre}',
    }
    return render(request, 'requerimientos/requerimiento_validar_lider_individual.html', context)


@login_required
def requerimiento_validar_cliente_individual(request, pk):
    """
    Vista para que el cliente valide un requerimiento específico.
    Muestra solo el requerimiento solicitado.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar que el usuario sea cliente del proyecto
    es_cliente = proyecto.clientes.filter(id=request.user.id).exists()
    if not es_cliente:
        messages.error(request, 'Solo los clientes del proyecto pueden validar requerimientos.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    # Verificar que el requerimiento esté en estado VALIDADO (validado por líder)
    if requerimiento.estado != 'VALIDADO':
        messages.info(request, 'Este requerimiento aún no ha sido validado por el líder.')
        return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        comentario = request.POST.get('comentario', '').strip()
        
        if accion == 'validar':
            # Aprobar el requerimiento
            requerimiento.estado = 'APROBADO'
            requerimiento.validado_cliente = True
            requerimiento.fecha_validacion_cliente = timezone.now()
            requerimiento.save()
            
            # Crear comentario si se proporcionó
            if comentario:
                ComentarioValidacion.objects.create(
                    requerimiento=requerimiento,
                    autor=request.user,
                    comentario=comentario,
                    tipo_accion='VALIDAR'
                )
            
            messages.success(request, f'✅ Requerimiento "{requerimiento.nombre}" aprobado exitosamente.')
            return redirect('requerimientos:requerimiento_detail', pk=pk)
            
        elif accion == 'rechazar':
            if not comentario:
                messages.error(request, 'Debes proporcionar un comentario al rechazar un requerimiento.')
            else:
                # Rechazar el requerimiento (vuelve a BORRADOR)
                requerimiento.estado = 'BORRADOR'
                requerimiento.requiere_discusion = True
                requerimiento.motivo_rechazo_cliente = comentario
                requerimiento.ultimo_rechazado_por_cliente = request.user
                requerimiento.fecha_ultimo_rechazo_cliente = timezone.now()
                requerimiento.save()
                
                # Crear comentario de rechazo
                ComentarioValidacion.objects.create(
                    requerimiento=requerimiento,
                    autor=request.user,
                    comentario=comentario,
                    tipo_accion='RECHAZAR'
                )
                
                messages.info(request, f'ℹ️ Requerimiento "{requerimiento.nombre}" rechazado para revisión.')
                return redirect('requerimientos:requerimiento_detail', pk=pk)
    
    context = {
        'proyecto': proyecto,
        'requerimiento': requerimiento,
        'page_title': f'Validar: {requerimiento.nombre}',
    }
    return render(request, 'requerimientos/requerimiento_validar_cliente_individual.html', context)


# ============================================================================
# VISTAS DE DISCUSIÓN Y COMENTARIOS
# ============================================================================

@login_required
def requerimiento_discusion(request, pk):
    """
    Vista para ver y participar en la discusión de validación de un requerimiento.
    Permite ver todos los comentarios y agregar respuestas en diferentes contextos.
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    proyecto = requerimiento.proyecto
    
    # Verificar permisos de acceso al requerimiento
    es_lider = request.user == proyecto.lider
    es_participante = ParticipacionProyecto.objects.filter(
        proyecto=proyecto,
        usuario=request.user
    ).exists()
    es_stakeholder = request.user.roles.filter(nombre__iexact='Stakeholder').exists() and \
                     proyecto.clientes.filter(id=request.user.id).exists()
    
    # Solo permitir acceso a miembros del proyecto
    if not (es_lider or es_participante or es_stakeholder):
        messages.error(request, '⛔ No tienes permisos para ver este requerimiento.')
        return redirect('dashboards:developer_dashboard')
    
    # Determinar permisos de comentario
    puede_comentar_interno = es_lider or es_participante
    puede_comentar_cliente = es_stakeholder or es_lider
    
    # Procesar formulario de nuevo comentario
    if request.method == 'POST':
        tipo_comentario = request.POST.get('tipo_comentario', 'DISCUSION_INTERNA')
        tipo_accion = request.POST.get('tipo_accion', 'RESPUESTA')
        comentario_texto = request.POST.get('comentario', '').strip()
        comentario_padre_id = request.POST.get('comentario_padre_id')
        imagen = request.FILES.get('imagen')
        link_externo = request.POST.get('link_externo', '').strip()
        
        # Validar permisos según tipo de comentario
        if tipo_comentario == 'DISCUSION_INTERNA' and not puede_comentar_interno:
            messages.error(request, '⛔ No tienes permisos para comentarios internos.')
        elif tipo_comentario == 'VALIDACION_CLIENTE' and not puede_comentar_cliente:
            messages.error(request, '⛔ No tienes permisos para comentarios con el cliente.')
        elif not comentario_texto:
            messages.error(request, '⚠️ El comentario no puede estar vacío.')
        else:
            # Crear el comentario
            comentario_padre = None
            if comentario_padre_id:
                comentario_padre = get_object_or_404(ComentarioValidacion, pk=comentario_padre_id)
            
            ComentarioValidacion.objects.create(
                requerimiento=requerimiento,
                autor=request.user,
                comentario=comentario_texto,
                tipo_accion=tipo_accion,
                tipo_comentario=tipo_comentario,
                comentario_padre=comentario_padre,
                imagen=imagen,
                link_externo=link_externo
            )
            
            messages.success(request, '✅ Comentario agregado correctamente.')
            return redirect('requerimientos:requerimiento_discusion', pk=pk)
    
    # Obtener comentarios organizados por tipo y jerarquía
    comentarios_internos = ComentarioValidacion.objects.filter(
        requerimiento=requerimiento,
        tipo_comentario='DISCUSION_INTERNA',
        comentario_padre__isnull=True
    ).select_related('autor').order_by('fecha_creacion')
    
    comentarios_cliente = ComentarioValidacion.objects.filter(
        requerimiento=requerimiento,
        tipo_comentario='VALIDACION_CLIENTE',
        comentario_padre__isnull=True
    ).select_related('autor').order_by('fecha_creacion')
    
    comentarios_implementacion = ComentarioValidacion.objects.filter(
        requerimiento=requerimiento,
        tipo_comentario='IMPLEMENTACION',
        comentario_padre__isnull=True
    ).select_related('autor').order_by('fecha_creacion')
    
    total_comentarios = ComentarioValidacion.objects.filter(requerimiento=requerimiento).count()
    
    context = {
        'page_title': f'Discusión - {requerimiento.nombre}',
        'requerimiento': requerimiento,
        'proyecto': proyecto,
        'comentarios_internos': comentarios_internos,
        'comentarios_cliente': comentarios_cliente,
        'comentarios_implementacion': comentarios_implementacion,
        'total_comentarios': total_comentarios,
        'puede_comentar_interno': puede_comentar_interno,
        'puede_comentar_cliente': puede_comentar_cliente,
        'es_lider': es_lider,
        'es_stakeholder': es_stakeholder,
    }
    
    return render(request, 'requerimientos/requerimiento_discusion.html', context)


# ============================================================================
# VISTAS DE GESTIÓN DE DEPENDENCIAS
# ============================================================================

@login_required
def requerimiento_dependencias(request, proyecto_id=None):
    """
    Vista para que líderes gestionen dependencias entre requerimientos.
    Permite definir qué requerimientos dependen de otros para planificación y priorización.
    """
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
        messages.error(request, 'Debe especificar un proyecto para gestionar dependencias.')
        return redirect('dashboards:lider_dashboard')
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Verificar que el usuario sea líder del proyecto
    if request.user != proyecto.lider:
        messages.error(request, 'Solo el líder del proyecto puede gestionar dependencias de requerimientos.')
        return redirect('dashboards:lider_dashboard')
    
    # Obtener todos los requerimientos del proyecto
    requerimientos = Requerimiento.objects.filter(
        proyecto=proyecto
    ).select_related('proyecto').prefetch_related('dependencias', 'dependientes').order_by('nombre')
    
    if request.method == 'POST':
        # Procesar las dependencias establecidas
        dependencias_actualizadas = 0
        dependencias_eliminadas = 0
        
        for req in requerimientos:
            # Obtener las dependencias seleccionadas para este requerimiento
            dependencias_seleccionadas = request.POST.getlist(f'dependencias_{req.pk}')
            
            # Contar dependencias antes de limpiar
            dependencias_antes = req.dependencias.count()
            
            # Limpiar dependencias actuales
            req.dependencias.clear()
            
            # Si se seleccionó la opción vacía ("Sin dependencias"), no agregar nada
            if '' in dependencias_seleccionadas or len(dependencias_seleccionadas) == 0:
                # Solo contar como eliminación si había dependencias antes
                if dependencias_antes > 0:
                    dependencias_eliminadas += dependencias_antes
            else:
                # Agregar nuevas dependencias (filtrando valores vacíos)
                for dep_id in dependencias_seleccionadas:
                    if dep_id:  # Saltar valores vacíos
                        try:
                            dep_id_int = int(dep_id)
                            # Evitar auto-dependencias
                            if dep_id_int != req.pk:
                                dependencia = Requerimiento.objects.get(pk=dep_id_int, proyecto=proyecto)
                                req.dependencias.add(dependencia)
                                dependencias_actualizadas += 1
                        except (ValueError, Requerimiento.DoesNotExist):
                            continue
        
        if dependencias_actualizadas > 0 or dependencias_eliminadas > 0:
            mensaje = []
            if dependencias_actualizadas > 0:
                mensaje.append(f'✅ Se establecieron {dependencias_actualizadas} dependencia(s)')
            if dependencias_eliminadas > 0:
                mensaje.append(f'🗑️ Se eliminaron {dependencias_eliminadas} dependencia(s)')
            messages.success(request, ' y '.join(mensaje) + '.')
        else:
            messages.info(request, 'No se realizaron cambios en las dependencias.')
        
        return redirect(f"{reverse('requerimientos:requerimiento_dependencias')}?proyecto_id={proyecto.pk}")
    
    # Preparar datos para el template
    requerimientos_con_info = []
    for req in requerimientos:
        # Obtener dependencias actuales (de los que depende este req)
        dependencias_actuales = list(req.dependencias.all())
        dependencias_ids = [d.pk for d in dependencias_actuales]
        
        # Obtener dependientes (requerimientos que dependen de este)
        dependientes_actuales = list(req.dependientes.all())
        
        # Requerimientos disponibles para ser dependencias (todos menos él mismo)
        disponibles = [r for r in requerimientos if r.pk != req.pk]
        
        requerimientos_con_info.append({
            'requerimiento': req,
            'dependencias_actuales': dependencias_actuales,
            'dependencias_ids': dependencias_ids,
            'dependientes': dependientes_actuales,
            'disponibles': disponibles,
        })
    
    context = {
        'proyecto': proyecto,
        'requerimientos_con_info': requerimientos_con_info,
        'total_requerimientos': requerimientos.count(),
        'page_title': f'{proyecto.nombre} - Gestión de Dependencias',
    }
    
    return render(request, 'requerimientos/requerimiento_dependencias.html', context)
