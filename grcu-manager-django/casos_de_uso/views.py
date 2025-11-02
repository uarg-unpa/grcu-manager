from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil
from .forms import CasoDeUsoUnificadoForm
from proyectos.models import Proyecto
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
    return render(request, "casos_de_uso/caso_de_uso_detail.html", {"caso": caso})


@login_required
def caso_de_uso_update(request, pk):
    """
    Vista para editar casos de uso según la metodología del proyecto.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto

    # Verificar permisos: solo líderes o participantes del proyecto
    es_lider = request.user == proyecto.lider
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()

    if not (es_lider or es_participante):
        messages.error(
            request,
            'No tienes permiso para editar casos de uso en este proyecto.'
        )
        return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)

    # Determinar formulario según metodología del proyecto
    es_tradicional = proyecto.metodologia == 'TRADICIONAL'
    es_agil = proyecto.metodologia == 'AGIL'

    if request.method == 'POST':
        # Instanciar el formulario apropiado
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
                        'prioridad': form.cleaned_data.get('prioridad', ''),
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
                    detalle.save()

            elif es_agil:
                detalle, created = DetalleCasoDeUsoAgil.objects.get_or_create(
                    caso_de_uso_padre=caso,
                    defaults={
                        'historia_usuario': form.cleaned_data.get('historia_usuario', ''),
                        'criterio_aceptacion': form.cleaned_data.get('criterio_aceptacion', ''),
                        'responsable': form.cleaned_data.get('responsable', ''),
                        'estado_scrum': form.cleaned_data.get('estado_scrum', ''),
                        'prioridad': form.cleaned_data.get('prioridad', ''),
                        'observaciones': form.cleaned_data.get('observaciones', '')
                    }
                )
                if not created:
                    detalle.historia_usuario = form.cleaned_data.get('historia_usuario', '')
                    detalle.criterio_aceptacion = form.cleaned_data.get('criterio_aceptacion', '')
                    detalle.responsable = form.cleaned_data.get('responsable', '')
                    detalle.estado_scrum = form.cleaned_data.get('estado_scrum', '')
                    detalle.observaciones = form.cleaned_data.get('observaciones', '')
                    detalle.save()

            messages.success(request, f'✅ Caso de Uso "{caso.nombre}" actualizado exitosamente.')
            return redirect('casos_de_uso:caso_de_uso_detail', pk=pk)
    else:
        # GET: Instanciar formulario con datos existentes
        initial_data = {
            'nombre': caso.nombre,
            'descripcion': caso.descripcion,
            'imagen': caso.imagen,
            'link_externo': caso.link_externo,
        }

        if es_tradicional:
            # Agregar datos del detalle tradicional si existe
            if hasattr(caso, 'detalle_tradicional') and caso.detalle_tradicional:
                initial_data.update({
                    'actor_principal': caso.detalle_tradicional.actor_principal,
                    'precondiciones': caso.detalle_tradicional.precondiciones,
                    'flujo_principal': caso.detalle_tradicional.flujo_principal,
                    'flujo_alternativo': caso.detalle_tradicional.flujo_alternativo,
                    'postcondiciones': caso.detalle_tradicional.postcondiciones,
                    'observaciones': caso.detalle_tradicional.observaciones,
                })
            form = CasoDeUsoUnificadoForm(initial=initial_data)
        elif es_agil:
            # Agregar datos del detalle ágil si existe
            if hasattr(caso, 'detalle_agil') and caso.detalle_agil:
                initial_data.update({
                    'historia_usuario': caso.detalle_agil.historia_usuario,
                    'criterio_aceptacion': caso.detalle_agil.criterio_aceptacion,
                    'responsable': caso.detalle_agil.responsable,
                    'estado_scrum': caso.detalle_agil.estado_scrum,
                    'observaciones': caso.detalle_agil.observaciones,
                })
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
        'is_edit': True
    }

    return render(request, 'casos_de_uso/caso_de_uso_create.html', context)


@login_required
def caso_de_uso_delete(request, pk):
    """
    Vista para eliminar casos de uso con confirmación.
    """
    caso = get_object_or_404(CasoDeUso, pk=pk)
    proyecto = caso.proyecto

    # Verificar permisos: solo líderes del proyecto pueden eliminar
    if request.user != proyecto.lider:
        messages.error(
            request,
            'Solo el líder del proyecto puede eliminar casos de uso.'
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
def caso_de_uso_create(request, proyecto_id=None):
    """
    Vista para crear un caso de uso. Utiliza el formulario unificado.
    """
    proyecto = None
    if proyecto_id:
        from proyectos.models import Proyecto
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        form = CasoDeUsoUnificadoForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el caso de uso base
            caso = CasoDeUso.objects.create(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data.get('descripcion', ''),
                proyecto=proyecto,
                creado_por=request.user,
                imagen=form.cleaned_data.get('imagen'),
                link_externo=form.cleaned_data.get('link_externo', '')
            )

            # Determinar la metodología del proyecto
            es_tradicional = proyecto.metodologia == 'TRADICIONAL' if proyecto else False
            es_agil = proyecto.metodologia == 'AGIL' if proyecto else False

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
            elif es_agil:
                DetalleCasoDeUsoAgil.objects.create(
                    caso_de_uso_padre=caso,
                    historia_usuario=form.cleaned_data.get('historia_usuario', ''),
                    criterio_aceptacion=form.cleaned_data.get('criterio_aceptacion', ''),
                    responsable=form.cleaned_data.get('responsable', ''),
                    estado_scrum=form.cleaned_data.get('estado_scrum', ''),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )

            messages.success(request, f'✅ Caso de Uso "{caso.nombre}" creado exitosamente.')
            return redirect('casos_de_uso:caso_de_uso_detail', pk=caso.pk)
    else:
        # Generar nombre automático CU-<número>
        initial_data = {}
        if proyecto:
            # Contar el número total de casos de uso en el proyecto
            total_casos = CasoDeUso.objects.filter(proyecto=proyecto).count()
            nuevo_num = total_casos + 1
            initial_data['nombre'] = f'CU-{nuevo_num:02d}'
        form = CasoDeUsoUnificadoForm(initial=initial_data)

    contexto = {
        'form': form,
        'proyecto': proyecto,
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
    
    # Comparar todos los campos importantes
    campos = [
        ('nombre', 'Nombre'),
        ('descripcion', 'Descripción'),
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
