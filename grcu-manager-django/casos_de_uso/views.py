from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil
from .forms import CasoDeUsoUnificadoForm
from proyectos.models import Proyecto
from requerimientos.models import Requerimiento
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

@login_required
def caso_de_uso_list(request, proyecto_id=None):
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        casos = CasoDeUso.objects.filter(proyecto=proyecto).select_related(
            'proyecto', 'detalle_tradicional', 'detalle_agil'
        )
    else:
        # Si el usuario es líder, mostrar solo el proyecto que lidera
        proyectos_liderados = getattr(request.user, 'lidera_proyectos', None)
        if proyectos_liderados and proyectos_liderados.exists():
            proyecto = proyectos_liderados.first()
            casos = CasoDeUso.objects.filter(proyecto=proyecto).select_related(
                'proyecto', 'detalle_tradicional', 'detalle_agil'
            )
        # Si es un developer, mostrar el proyecto en el que participa
        elif request.user.es_desarrollador():
            proyectos_participa = Proyecto.objects.filter(participantes=request.user)
            if proyectos_participa.exists():
                proyecto = proyectos_participa.first()
                casos = CasoDeUso.objects.filter(proyecto=proyecto).select_related(
                    'proyecto', 'detalle_tradicional', 'detalle_agil'
                )
            else:
                casos = CasoDeUso.objects.all().select_related(
                    'proyecto', 'detalle_tradicional', 'detalle_agil'
                )
                proyecto = None
        else:
            casos = CasoDeUso.objects.all().select_related(
                'proyecto', 'detalle_tradicional', 'detalle_agil'
            )
            proyecto = None
    if proyecto:
        page_title = f"{proyecto.nombre} - Casos de Uso"
    else:
        page_title = "Casos de Uso"
    return render(request, "casos_de_uso/caso_de_uso_list.html", {"casos": casos, "proyecto": proyecto, "page_title": page_title})

@login_required
def caso_de_uso_detail(request, pk):
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto
    
    # Verificar permisos del usuario
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    
    context = {
        'caso': caso,
        'proyecto': proyecto,
        'es_lider': es_lider,
        'es_participante': es_participante,
    }
    
    return render(request, "casos_de_uso/caso_de_uso_detail.html", context)


@login_required
def caso_de_uso_update(request, pk):
    """
    Vista para editar casos de uso según la metodología del proyecto.
    Solo el creador del caso de uso o el líder del proyecto pueden editar.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto

    # Verificar permisos: solo líder o creador del caso de uso
    es_lider = request.user == proyecto.lider
    es_creador = request.user == caso.creado_por

    if not (es_lider or es_creador):
        messages.error(
            request,
            f'⛔ Solo el creador ({caso.creado_por.nombre if caso.creado_por else "N/A"}) o el líder del proyecto '
            f'pueden editar este caso de uso.'
        )
        return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)

    # Determinar formulario según metodología del proyecto
    es_tradicional = proyecto.metodologia == 'TRADICIONAL'
    es_agil = proyecto.metodologia == 'AGIL'

    if request.method == 'POST':
        # Instanciar el formulario apropiado con datos POST y archivos
        if es_tradicional:
            form = CasoDeUsoUnificadoForm(request.POST, request.FILES)
        elif es_agil:
            form = CasoDeUsoUnificadoForm(request.POST, request.FILES)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)

        if form.is_valid():
            # Actualizar el caso de uso base
            caso.nombre = form.cleaned_data['nombre']
            caso.descripcion = form.cleaned_data.get('descripcion', '')
            nueva_imagen = form.cleaned_data.get('imagen')
            if nueva_imagen:
                caso.imagen = nueva_imagen
            caso.link_externo = form.cleaned_data.get('link_externo', '')
            caso._history_user = request.user
            caso.save()

            # Actualizar o crear el detalle específico según la metodología
            if es_tradicional:
                detalle, created = DetalleCasoDeUsoTradicional.objects.get_or_create(
                    caso_de_uso_padre=caso,
                    defaults={
                        'actor_principal': form.cleaned_data.get('actor_principal', ''),
                        'precondiciones': form.cleaned_data.get('precondiciones', ''),
                        'flujo_principal': form.cleaned_data.get('flujo_principal', ''),
                        'flujo_alternativo': form.cleaned_data.get('flujo_alternativo', ''),
                        'postcondiciones': form.cleaned_data.get('postcondiciones', ''),
                        'observaciones': form.cleaned_data.get('observaciones', '')
                    }
                )
                if not created:
                    detalle.actor_principal = form.cleaned_data.get('actor_principal', '')
                    detalle.precondiciones = form.cleaned_data.get('precondiciones', '')
                    detalle.flujo_principal = form.cleaned_data.get('flujo_principal', '')
                    detalle.flujo_alternativo = form.cleaned_data.get('flujo_alternativo', '')
                    detalle.postcondiciones = form.cleaned_data.get('postcondiciones', '')
                    detalle.observaciones = form.cleaned_data.get('observaciones', '')
                    detalle._history_user = request.user
                    detalle.save()

            elif es_agil:
                detalle, created = DetalleCasoDeUsoAgil.objects.get_or_create(
                    caso_de_uso_padre=caso,
                    defaults={
                        'historia_usuario': form.cleaned_data.get('historia_usuario', ''),
                        'criterio_aceptacion': form.cleaned_data.get('criterio_aceptacion', ''),
                        'responsable': form.cleaned_data.get('responsable', ''),
                        'estado_scrum': form.cleaned_data.get('estado_scrum', ''),
                        'observaciones': form.cleaned_data.get('observaciones', '')
                    }
                )
                if not created:
                    detalle.historia_usuario = form.cleaned_data.get('historia_usuario', '')
                    detalle.criterio_aceptacion = form.cleaned_data.get('criterio_aceptacion', '')
                    detalle.responsable = form.cleaned_data.get('responsable', '')
                    detalle.estado_scrum = form.cleaned_data.get('estado_scrum', '')
                    detalle.observaciones = form.cleaned_data.get('observaciones', '')
                    detalle._history_user = request.user
                    detalle.save()

            messages.success(request, f'✅ Caso de Uso "{caso.nombre}" actualizado exitosamente.')
            return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)
        else:
            # Si el formulario no es válido, se mantendrá con los datos POST
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        # GET: Instanciar formulario con datos existentes
        initial_data = {
            'identificador': caso.identificador,
            'nombre': caso.nombre,
            'descripcion': caso.descripcion,
            'link_externo': caso.link_externo,
        }

        if es_tradicional:
            # Agregar datos del detalle tradicional si existe
            try:
                detalle = caso.detalle_tradicional_reverse
                initial_data.update({
                    'actor_principal': detalle.actor_principal,
                    'precondiciones': detalle.precondiciones,
                    'flujo_principal': detalle.flujo_principal,
                    'flujo_alternativo': detalle.flujo_alternativo,
                    'postcondiciones': detalle.postcondiciones,
                    'observaciones': detalle.observaciones,
                })
            except DetalleCasoDeUsoTradicional.DoesNotExist:
                pass  # No hay detalle, se usarán campos vacíos
            
            form = CasoDeUsoUnificadoForm(initial=initial_data)
            
        elif es_agil:
            # Agregar datos del detalle ágil si existe
            try:
                detalle = caso.detalle_agil_reverse
                initial_data.update({
                    'historia_usuario': detalle.historia_usuario,
                    'criterio_aceptacion': detalle.criterio_aceptacion,
                    'responsable': detalle.responsable,
                    'estado_scrum': detalle.estado_scrum,
                    'observaciones': detalle.observaciones,
                })
            except DetalleCasoDeUsoAgil.DoesNotExist:
                pass  # No hay detalle, se usarán campos vacíos
            
            form = CasoDeUsoUnificadoForm(initial=initial_data)
        else:
            messages.error(request, 'Metodología no reconocida.')
            return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)

    page_title = f"{proyecto.nombre} - Editar Caso de Uso: {caso.nombre}"

    context = {
        'form': form,
        'caso': caso,
        'proyecto': proyecto,
        'es_tradicional': es_tradicional,
        'es_agil': es_agil,
        'metodologia_display': proyecto.get_metodologia_display(),
        'page_title': page_title,
        'is_edit': True,
        'imagen_existente': caso.imagen,  # Para mostrar la imagen actual
    }

    return render(request, 'casos_de_uso/crear.html', context)


@login_required
def caso_de_uso_delete(request, pk):
    """
    Vista para eliminar casos de uso con confirmación.
    Solo el creador del caso de uso o el líder del proyecto pueden eliminar.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto

    # Verificar permisos: solo líder o creador del caso de uso
    es_lider = request.user == proyecto.lider
    es_creador = request.user == caso.creado_por
    
    if not (es_lider or es_creador):
        messages.error(
            request,
            f'⛔ Solo el creador ({caso.creado_por.nombre if caso.creado_por else "N/A"}) o el líder del proyecto '
            f'pueden eliminar este caso de uso.'
        )
        return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)

    if request.method == 'POST':
        nombre_caso = caso.nombre
        caso.delete()
        messages.success(request, f'✅ Caso de Uso "{nombre_caso}" eliminado exitosamente.')
        return redirect('casos_de_uso:caso_de_uso_list')

    context = {
        'caso': caso,
        'proyecto': proyecto,
        'page_title': f'{proyecto.nombre} - Eliminar Caso de Uso: {caso.nombre}',
    }

    return render(request, 'casos_de_uso/caso_de_uso_delete.html', context)


@login_required
def caso_de_uso_create(request, proyecto_id=None, requerimiento_id=None):
    """
    Vista para crear un caso de uso. Utiliza el formulario unificado.
    Si se proporciona requerimiento_id, valida que el requerimiento esté VALIDADO.
    """
    proyecto = None
    requerimiento = None
    
    if proyecto_id:
        from proyectos.models import Proyecto
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if requerimiento_id:
        requerimiento = get_object_or_404(Requerimiento, id=requerimiento_id)
        
        # Validar que el requerimiento pertenezca al proyecto
        if proyecto and requerimiento.proyecto != proyecto:
            messages.error(request, 'El requerimiento no pertenece a este proyecto.')
            return redirect('requerimientos:requerimiento_detail', pk=requerimiento_id)
        
        # Aplicar la regla de oro: el requerimiento debe estar VALIDADO
        if requerimiento.estado != 'VALIDADO':
            estado_display = dict(Requerimiento.ESTADO_CHOICES).get(requerimiento.estado, requerimiento.estado)
            messages.error(
                request,
                f'No se puede crear un caso de uso para un requerimiento en estado "{estado_display}". '
                'El requerimiento debe estar VALIDADO primero.'
            )
            return redirect('requerimientos:requerimiento_detail', pk=requerimiento_id)
        
        # Si no hay proyecto especificado, usar el del requerimiento
        if not proyecto:
            proyecto = requerimiento.proyecto

    if request.method == 'POST':
        form = CasoDeUsoUnificadoForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el caso de uso base
            caso = CasoDeUso(
                identificador=form.cleaned_data.get('identificador', ''),
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                proyecto=proyecto,
                creado_por=request.user,
                imagen=form.cleaned_data.get('imagen'),
                link_externo=form.cleaned_data.get('link_externo', ''),
                requerimiento=requerimiento  # Asociar con el requerimiento si existe
            )
            # Asignar usuario al historial
            caso._history_user = request.user
            caso.save()

            # Determinar la metodología del proyecto
            es_tradicional = proyecto.metodologia == 'TRADICIONAL' if proyecto else False
            es_agil = proyecto.metodologia == 'AGIL' if proyecto else False

            # Crear el detalle específico según la metodología
            if es_tradicional:
                detalle = DetalleCasoDeUsoTradicional(
                    caso_de_uso_padre=caso,
                    actor_principal=form.cleaned_data.get('actor_principal', ''),
                    precondiciones=form.cleaned_data.get('precondiciones', ''),
                    flujo_principal=form.cleaned_data.get('flujo_principal', ''),
                    flujo_alternativo=form.cleaned_data.get('flujo_alternativo', ''),
                    postcondiciones=form.cleaned_data.get('postcondiciones', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                detalle._history_user = request.user
                detalle.save()
            elif es_agil:
                detalle = DetalleCasoDeUsoAgil(
                    caso_de_uso_padre=caso,
                    historia_usuario=form.cleaned_data.get('historia_usuario', ''),
                    criterio_aceptacion=form.cleaned_data.get('criterio_aceptacion', ''),
                    responsable=form.cleaned_data.get('responsable', ''),
                    estado_scrum=form.cleaned_data.get('estado_scrum', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                detalle._history_user = request.user
                detalle.save()
            
            # ⚡ CREAR RELACIÓN EN TABLA INTERMEDIA si se creó desde un requerimiento
            if requerimiento:
                from requerimientos.models import RequerimientoCaso
                RequerimientoCaso.objects.create(
                    requerimiento=requerimiento,
                    caso_de_uso=caso,
                    nota=f'Caso de uso creado desde el requerimiento {requerimiento.nombre}'
                )

            messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado exitosamente.')
            
            # Redirigir al detalle del requerimiento si se creó desde ahí, sino al listado
            if requerimiento:
                return redirect('requerimientos:requerimiento_detail', pk=requerimiento.pk)
            else:
                return redirect('casos_de_uso:caso_de_uso_list', proyecto_id=proyecto.id)
        else:
            # Si el formulario no es válido, se mantendrá con los datos POST
            # Los valores ingresados se conservarán para que el usuario los corrija
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        # Generar identificador automático CU-<número>
        initial_data = {}
        if proyecto:
            # Obtener el último CU del proyecto
            ultimo_cu = CasoDeUso.objects.filter(proyecto=proyecto).order_by('-id').first()
            if ultimo_cu and ultimo_cu.identificador:
                # Extraer el número del identificador (ej: CU-001 -> 1)
                try:
                    ultimo_numero = int(ultimo_cu.identificador.split('-')[-1])
                    nuevo_numero = ultimo_numero + 1
                except (ValueError, IndexError):
                    nuevo_numero = CasoDeUso.objects.filter(proyecto=proyecto).count() + 1
            else:
                nuevo_numero = CasoDeUso.objects.filter(proyecto=proyecto).count() + 1
            
            initial_data['identificador'] = f'CU-{nuevo_numero:03d}'
        form = CasoDeUsoUnificadoForm(initial=initial_data)

    contexto = {
        'form': form,
        'proyecto': proyecto,
        'requerimiento': requerimiento,
    }
    return render(request, 'casos_de_uso/crear.html', contexto)


@login_required
def buscar_casos_de_uso_ajax(request):
    """Endpoint AJAX para búsqueda de casos de uso"""
    search_query = request.GET.get('q', '').strip()
    proyecto_id = request.GET.get('proyecto_id', '').strip()
    
    # Construir filtros
    filtros = Q()
    
    if search_query:
        filtros &= (
            Q(nombre__icontains=search_query) | 
            Q(descripcion__icontains=search_query)
        )
    
    if proyecto_id:
        filtros &= Q(proyecto_id=proyecto_id)
    
    # Si no hay filtros, devolver vacío
    if not (search_query or proyecto_id):
        return JsonResponse({'casos': [], 'count': 0})
    
    # Buscar casos de uso con prefetch_related para optimizar
    casos = CasoDeUso.objects.filter(filtros).select_related(
        'proyecto'
    ).order_by('nombre')[:100]
    
    # Serializar casos de uso
    casos_data = []
    for caso in casos:
        # Truncar descripción
        descripcion = caso.descripcion if caso.descripcion else ''
        if len(descripcion) > 60:
            descripcion = descripcion[:57] + '...'
        
        casos_data.append({
            'id': caso.pk,
            'nombre': caso.nombre,
            'descripcion': descripcion,
        })
        
    return JsonResponse({
        'casos': casos_data,
        'count': len(casos_data)
    })

@login_required
def caso_de_uso_historial(request, pk):
    """
    Muestra el historial completo de versiones de un caso de uso.
    Solo usuarios con acceso al proyecto pueden ver el historial.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto
    
    # Verificar permisos: solo líderes o participantes del proyecto
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(pk=request.user.pk).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para ver el historial de este caso de uso.")
        return redirect('proyectos:lista_proyectos')
    
    # Obtener historial ordenado por fecha (más reciente primero)
    historial = caso.history.all().order_by('-history_date')  # type: ignore[attr-defined]
    
    # Preparar datos de versiones con información del cambio
    versiones = []
    for idx, version in enumerate(historial):
        # Calcular número de versión (más reciente = 1)
        numero_version = len(historial) - idx
        
        # Información del usuario que hizo el cambio
        usuario = version.history_user if version.history_user else None
        usuario_nombre = usuario.nombre if usuario else 'No registrado'
        
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
        'caso': caso,
        'proyecto': proyecto,
        'versiones': versiones,
        'total_versiones': len(versiones),
        'page_title': f'{proyecto.nombre} - Historial de {caso.nombre}',
    }
    
    return render(request, 'casos_de_uso/historial.html', context)


@login_required
def caso_de_uso_version_detail(request, pk, history_id):
    """
    Muestra los detalles de una versión específica del caso de uso.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto
    
    # Verificar permisos
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(pk=request.user.pk).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para ver esta información.")
        return redirect('proyectos:lista_proyectos')
    
    # Obtener la versión histórica específica
    version = get_object_or_404(
        caso.history.model,  # type: ignore[attr-defined]
        history_id=history_id,
        id=pk
    )
    
    # Calcular número de versión
    historial_completo = caso.history.all().order_by('-history_date')  # type: ignore[attr-defined]
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
        'caso': caso,
        'proyecto': proyecto,
        'version': version,
        'numero_version': numero_version,
        'tipo_cambio': tipo_cambio,
        'cambios': cambios,
        'version_anterior': version_anterior,
        'page_title': f'{proyecto.nombre} - Versión #{numero_version} de {caso.nombre}',
    }
    
    return render(request, 'casos_de_uso/version_detail.html', context)


@login_required
def caso_de_uso_comparar_versiones(request, pk):
    """
    Compara dos versiones específicas del caso de uso.
    Recibe version1_id y version2_id por GET.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto
    
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
        return redirect('casos_de_uso:caso_de_uso_historial', pk=pk)
    
    # Obtener versiones
    try:
        version1 = caso.history.get(history_id=history_id_1)  # type: ignore[attr-defined]
        version2 = caso.history.get(history_id=history_id_2)  # type: ignore[attr-defined]
    except:
        messages.error(request, "Una o ambas versiones no existen.")
        return redirect('casos_de_uso:caso_de_uso_historial', pk=pk)
    
    # Asegurar que version1 es la más antigua
    if version1.history_date > version2.history_date:
        version1, version2 = version2, version1
    
    # Calcular números de versión
    historial_completo = caso.history.all().order_by('-history_date')  # type: ignore[attr-defined]
    numero_v1 = None
    numero_v2 = None
    
    for idx, v in enumerate(historial_completo):
        if v.history_id == version1.history_id:
            numero_v1 = len(historial_completo) - idx
        if v.history_id == version2.history_id:
            numero_v2 = len(historial_completo) - idx
    
    # Comparar todos los campos importantes del caso de uso base
    campos = [
        ('identificador', 'Identificador'),
        ('nombre', 'Nombre'),
        ('descripcion', 'Descripción'),
        ('link_externo', 'Enlace externo'),
    ]
    
    diferencias = []
    for campo, etiqueta in campos:
        valor_v1 = getattr(version1, campo, '') or ''
        valor_v2 = getattr(version2, campo, '') or ''
        
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
    
    # Comparar campos del detalle según la metodología
    if proyecto.metodologia == 'TRADICIONAL':
        # Obtener detalles tradicionales de ambas versiones
        detalle_v1 = DetalleCasoDeUsoTradicional.history.filter(
            caso_de_uso_padre_id=caso.pk,
            history_date__lte=version1.history_date
        ).order_by('-history_date').first()
        
        detalle_v2 = DetalleCasoDeUsoTradicional.history.filter(
            caso_de_uso_padre_id=caso.pk,
            history_date__lte=version2.history_date
        ).order_by('-history_date').first()
        
        if detalle_v1 or detalle_v2:
            campos_detalle = [
                ('actor_principal', 'Actor Principal'),
                ('precondiciones', 'Precondiciones'),
                ('flujo_principal', 'Flujo Principal'),
                ('flujo_alternativo', 'Flujo Alternativo'),
                ('postcondiciones', 'Postcondiciones'),
                ('observaciones', 'Observaciones'),
            ]
            
            for campo, etiqueta in campos_detalle:
                valor_v1 = getattr(detalle_v1, campo, '') if detalle_v1 else ''
                valor_v2 = getattr(detalle_v2, campo, '') if detalle_v2 else ''
                valor_v1 = valor_v1 or ''
                valor_v2 = valor_v2 or ''
                
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
    
    elif proyecto.metodologia == 'AGIL':
        # Obtener detalles ágiles de ambas versiones
        detalle_v1 = DetalleCasoDeUsoAgil.history.filter(
            caso_de_uso_padre_id=caso.pk,
            history_date__lte=version1.history_date
        ).order_by('-history_date').first()
        
        detalle_v2 = DetalleCasoDeUsoAgil.history.filter(
            caso_de_uso_padre_id=caso.pk,
            history_date__lte=version2.history_date
        ).order_by('-history_date').first()
        
        if detalle_v1 or detalle_v2:
            campos_detalle = [
                ('historia_usuario', 'Historia de Usuario'),
                ('criterio_aceptacion', 'Criterio de Aceptación'),
                ('responsable', 'Responsable'),
                ('estado_scrum', 'Estado Scrum'),
                ('observaciones', 'Observaciones'),
            ]
            
            for campo, etiqueta in campos_detalle:
                valor_v1 = getattr(detalle_v1, campo, '') if detalle_v1 else ''
                valor_v2 = getattr(detalle_v2, campo, '') if detalle_v2 else ''
                valor_v1 = valor_v1 or ''
                valor_v2 = valor_v2 or ''
                
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
        'caso': caso,
        'proyecto': proyecto,
        'version1': version1,
        'version2': version2,
        'numero_v1': numero_v1,
        'numero_v2': numero_v2,
        'diferencias': diferencias,
        'cambios_count': sum(1 for d in diferencias if d['cambio']),
        'page_title': f'{proyecto.nombre} - Comparar versiones de {caso.nombre}',
    }
    
    return render(request, 'casos_de_uso/comparar_versiones.html', context)
