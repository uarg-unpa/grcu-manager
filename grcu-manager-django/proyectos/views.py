from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from proyectos.models import Proyecto, ParticipacionProyecto
from proyectos.forms import ProyectoCrearForm
from roles.models import Rol
from accounts.models import Usuario
from grupos.models import Grupo
from django.core.paginator import Paginator
from django.db.models import Q


# Helpers
def is_admin(user):
    return user.roles.filter(nombre__iexact="Admin").exists()


def actualizar_rol_lider(usuario):
    """
    Actualiza automáticamente el rol de un usuario según si lidera proyectos o no.
    
    Reglas:
    - Si el usuario lidera AL MENOS UN proyecto → rol "Líder"
    - Si el usuario NO lidera ningún proyecto → rol "Desarrollador"
    - Los usuarios con rol "Admin" NO se ven afectados (no pueden ser líderes)
    """
    # No modificar el rol de administradores
    if usuario.roles.filter(nombre__iexact="Admin").exists():
        return
    
    # Obtener roles
    rol_lider = Rol.objects.get(nombre="Líder")
    rol_developer = Rol.objects.get(nombre="Desarrollador")
    
    # Verificar si el usuario lidera algún proyecto
    lidera_proyectos = Proyecto.objects.filter(lider=usuario).exists()
    
    if lidera_proyectos:
        # Debe tener rol "Líder"
        if not usuario.roles.filter(nombre="Líder").exists():
            # Cambiar de Desarrollador → Líder
            usuario.roles.remove(rol_developer)
            usuario.roles.add(rol_lider)
    else:
        # NO lidera proyectos, debe tener rol "Desarrollador"
        if usuario.roles.filter(nombre="Líder").exists():
            # Cambiar de Líder → Desarrollador
            usuario.roles.remove(rol_lider)
            usuario.roles.add(rol_developer)

@login_required
@user_passes_test(is_admin)
def lista_proyectos(request):
    proyectos = Proyecto.objects.select_related('lider', 'grupo').all()
    return render(request, "proyectos/lista_proyectos.html", {
        "proyectos": proyectos,
        "page_title": "Lista de Proyectos"
    })


@login_required
@user_passes_test(is_admin)
def crear_proyecto(request):
    if request.method == "POST":
        form = ProyectoCrearForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el proyecto
            proyecto = form.save(commit=False)
            proyecto.creado_por = request.user
            proyecto.save()

            # Obtener el grupo seleccionado (puede ser None)
            grupo = proyecto.grupo

            if grupo:
                # Solo procesar líder y participantes si hay grupo
                lider_id = form.cleaned_data.get('lider')
                if lider_id:
                    lider = Usuario.objects.get(id=lider_id)

                    # Validar que el líder no sea Admin
                    if lider.roles.filter(nombre__iexact="Admin").exists():
                        messages.error(request, "Un usuario con rol 'Admin' no puede ser líder de proyecto.")
                        return render(request, "proyectos/crear_proyecto.html", {
                            "form": form,
                            "page_title": "Crear Proyecto"
                        })

                    # Crear rol "Líder" si no existe
                    rol_lider, _ = Rol.objects.get_or_create(
                        nombre="Líder",
                        defaults={"color": "#28a745"}
                    )

                    # Asignar líder al proyecto
                    proyecto.lider = lider
                    proyecto.save()

                    # ⚡ ACTUALIZAR ROL DEL LÍDER (Developer → Líder)
                    actualizar_rol_lider(lider)

                    # Agregar líder con rol "Líder"
                    ParticipacionProyecto.objects.create(
                        usuario=lider,
                        proyecto=proyecto,
                        rol=rol_lider
                    )

                    # Agregar todos los demás integrantes del grupo como "Desarrollador"
                    rol_dev, _ = Rol.objects.get_or_create(
                        nombre="Desarrollador",
                        defaults={"color": "#ffc107"}
                    )

                    for integrante in grupo.integrantes.exclude(id=lider_id):
                        ParticipacionProyecto.objects.create(
                            usuario=integrante,
                            proyecto=proyecto,
                            rol=rol_dev
                        )

                messages.success(request, f"Proyecto '{proyecto.nombre}' creado exitosamente con el grupo '{grupo.nombre}'.")
            else:
                # Proyecto sin grupo
                messages.success(request, f"Proyecto '{proyecto.nombre}' creado exitosamente sin grupo asignado.")

            return redirect("proyectos:lista_proyectos")
    else:
        form = ProyectoCrearForm()

    return render(request, "proyectos/crear_proyecto.html", {
        "form": form,
        "page_title": "Crear Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == "POST":
        form = ProyectoCrearForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            proyecto = form.save()

            # Obtener el grupo seleccionado (puede ser None)
            grupo = proyecto.grupo

            if grupo:
                # Solo procesar líder y participantes si hay grupo
                lider_id = form.cleaned_data.get('lider')
                if lider_id:
                    lider = Usuario.objects.get(id=lider_id)
                    
                    # Validar que el líder no sea Admin
                    if lider.roles.filter(nombre__iexact="Admin").exists():
                        messages.error(request, "Un usuario con rol 'Admin' no puede ser líder de proyecto.")
                        return render(request, "proyectos/editar_proyecto.html", {
                            "form": form,
                            "proyecto": proyecto,
                            "page_title": "Editar Proyecto"
                        })

                    # Guardar el líder anterior para actualizar su rol después
                    lider_anterior = proyecto.lider

                    # Crear rol "Líder" si no existe
                    rol_lider, _ = Rol.objects.get_or_create(
                        nombre="Líder",
                        defaults={"color": "#28a745"}
                    )

                    # Asignar líder al proyecto
                    proyecto.lider = lider
                    proyecto.save()

                    # ⚡ ACTUALIZAR ROL DEL NUEVO LÍDER (Developer → Líder)
                    actualizar_rol_lider(lider)

                    # ⚡ ACTUALIZAR ROL DEL LÍDER ANTERIOR (Líder → Developer si ya no lidera proyectos)
                    if lider_anterior and lider_anterior != lider:
                        actualizar_rol_lider(lider_anterior)

                    # Limpiar participantes actuales
                    proyecto.participantes.clear()

                    # Agregar líder con rol "Líder"
                    ParticipacionProyecto.objects.create(
                        usuario=lider,
                        proyecto=proyecto,
                        rol=rol_lider
                    )

                    # Agregar todos los demás integrantes del grupo como "Desarrollador"
                    rol_dev, _ = Rol.objects.get_or_create(
                        nombre="Desarrollador",
                        defaults={"color": "#ffc107"}
                    )

                    for integrante in grupo.integrantes.exclude(id=lider_id):
                        ParticipacionProyecto.objects.create(
                            usuario=integrante,
                            proyecto=proyecto,
                            rol=rol_dev
                        )

                messages.success(request, f"Proyecto '{proyecto.nombre}' actualizado exitosamente con el grupo '{grupo.nombre}'.")
            else:
                # Proyecto sin grupo - guardar líder anterior y limpiar
                lider_anterior = proyecto.lider
                
                proyecto.lider = None
                proyecto.save()
                proyecto.participantes.clear()
                
                # ⚡ ACTUALIZAR ROL DEL LÍDER ANTERIOR (Líder → Developer si ya no lidera proyectos)
                if lider_anterior:
                    actualizar_rol_lider(lider_anterior)
                
                messages.success(request, f"Proyecto '{proyecto.nombre}' actualizado exitosamente sin grupo asignado.")

            return redirect("proyectos:lista_proyectos")
    else:
        form = ProyectoCrearForm(instance=proyecto)

    return render(request, "proyectos/editar_proyecto.html", {
        "form": form,
        "proyecto": proyecto,
        "page_title": "Editar Proyecto"
    })


@login_required
@user_passes_test(is_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == "POST":
        # Guardar el líder antes de eliminar el proyecto
        lider_anterior = proyecto.lider
        
        proyecto.delete()
        
        # ⚡ ACTUALIZAR ROL DEL LÍDER (Líder → Developer si ya no lidera proyectos)
        if lider_anterior:
            actualizar_rol_lider(lider_anterior)
        
        messages.success(request, f"Proyecto '{proyecto.nombre}' eliminado correctamente.")
        return redirect("proyectos:lista_proyectos")

    return render(request, "proyectos/confirmar_eliminar_proyecto.html", {
        "proyecto": proyecto,
        "page_title": "Eliminar Proyecto"
    })


def is_lider_del_proyecto(user, proyecto):
    """Helper para verificar si el usuario es líder del proyecto"""
    return proyecto.lider == user


@login_required
def asignar_metodologia(request, proyecto_id):
    """
    Vista para que el líder asigne o cambie la metodología del proyecto.
    Solo se permite cambiar si NO hay requerimientos cargados.
    """
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Verificar que el usuario sea el líder del proyecto
    if not is_lider_del_proyecto(request.user, proyecto):
        messages.error(request, "No tienes permiso para modificar este proyecto. Solo el líder puede asignar la metodología.")
        return redirect("dashboards:lider_dashboard")
    
    # Verificar si se puede cambiar la metodología
    if not proyecto.necesita_metodologia() and not proyecto.puede_cambiar_metodologia():
        messages.error(request, "No puedes cambiar la metodología porque el proyecto ya tiene requerimientos cargados.")
        return redirect("dashboards:lider_dashboard")
    
    if request.method == "POST":
        metodologia = request.POST.get('metodologia')
        
        if metodologia in ['TRADICIONAL', 'AGIL']:
            proyecto.metodologia = metodologia
            proyecto.save()
            
            metodologia_nombre = "Tradicional" if metodologia == "TRADICIONAL" else "Ágil"
            messages.success(request, f"Metodología '{metodologia_nombre}' asignada correctamente al proyecto '{proyecto.nombre}'.")
            return redirect("dashboards:lider_dashboard")
        else:
            messages.error(request, "Metodología inválida seleccionada.")
    
    return render(request, "proyectos/asignar_metodologia.html", {
        "proyecto": proyecto,
        "puede_cambiar": proyecto.puede_cambiar_metodologia(),
        "necesita_metodologia": proyecto.necesita_metodologia(),
        "page_title": "Asignar Metodología"
    })


@login_required
def matriz_trazabilidad(request, proyecto_id):
    """
    Vista de Matriz de Trazabilidad con Live Traceability.
    Muestra relaciones dinámicas entre requerimientos y casos de uso.
    Accesible por líder y participantes del proyecto.
    """
    from requerimientos.models import Requerimiento, RequerimientoCaso
    from casos_de_uso.models import CasoDeUso
    from django.db.models import Prefetch, Count
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Verificar permisos: líder o participante del proyecto
    es_lider = proyecto.lider == request.user
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para ver la matriz de trazabilidad de este proyecto.")
        return redirect("dashboards:lider_dashboard")
    
    # Filtros
    tipo_req = request.GET.get('tipo_req')
    estado_req = request.GET.get('estado_req')
    solo_huerfanos = request.GET.get('solo_huerfanos') == 'true'
    solo_sin_cubrir = request.GET.get('solo_sin_cubrir') == 'true'
    
    # Obtener requerimientos con filtros
    requerimientos_qs = Requerimiento.objects.filter(proyecto=proyecto)
    
    if tipo_req:
        requerimientos_qs = requerimientos_qs.filter(tipo=tipo_req)
    if estado_req:
        requerimientos_qs = requerimientos_qs.filter(estado=estado_req)
    if solo_huerfanos:
        requerimientos_qs = requerimientos_qs.annotate(
            rel_count=Count('relaciones_casos')
        ).filter(rel_count=0)
    
    # Prefetch optimizado para relaciones
    requerimientos = requerimientos_qs.prefetch_related(
        Prefetch('relaciones_casos',
                queryset=RequerimientoCaso.objects.select_related('caso_de_uso'))
    ).order_by('id')
    
    # Obtener casos de uso del proyecto
    casos = CasoDeUso.objects.filter(proyecto=proyecto).prefetch_related(
        Prefetch('relaciones_requerimientos',
                queryset=RequerimientoCaso.objects.select_related('requerimiento'))
    ).order_by('id')
    
    if solo_sin_cubrir:
        casos = casos.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
    
    # Construir matriz de trazabilidad
    matriz = []
    for req in requerimientos:
        fila = {
            'requerimiento': req,
            'relaciones': {}
        }
        # Obtener casos relacionados desde la tabla intermedia
        relaciones_req = req.relaciones_casos.all()  # type: ignore[attr-defined]
        for rel in relaciones_req:
            fila['relaciones'][rel.caso_de_uso.id] = {
                'relacionado': True,
                'fecha': rel.fecha_vinculacion,
                'nota': rel.nota
            }
        matriz.append(fila)
    
    # Calcular métricas
    total_requerimientos = requerimientos.count()
    total_casos = casos.count()
    total_relaciones = RequerimientoCaso.objects.filter(
        requerimiento__proyecto=proyecto
    ).count()
    
    # Cobertura
    reqs_con_casos = requerimientos.annotate(
        rel_count=Count('relaciones_casos')
    ).filter(rel_count__gt=0).count()
    
    casos_con_reqs = casos.annotate(
        rel_count=Count('relaciones_requerimientos')
    ).filter(rel_count__gt=0).count()
    
    cobertura_reqs = (reqs_con_casos / total_requerimientos * 100) if total_requerimientos > 0 else 0
    cobertura_casos = (casos_con_reqs / total_casos * 100) if total_casos > 0 else 0
    
    # Requerimientos por estado
    req_por_estado = {}
    for estado, label in Requerimiento.ESTADO_CHOICES:
        count = requerimientos.filter(estado=estado).count()
        req_por_estado[estado] = {
            'label': label,
            'count': count,
            'porcentaje': (count / total_requerimientos * 100) if total_requerimientos > 0 else 0
        }
    
    # Requerimientos por tipo
    req_por_tipo = {}
    for tipo, label in Requerimiento.TIPO_CHOICES:
        count = requerimientos.filter(tipo=tipo).count()
        req_por_tipo[tipo] = {
            'label': label,
            'count': count,
            'porcentaje': (count / total_requerimientos * 100) if total_requerimientos > 0 else 0
        }
    
    # Huérfanos
    reqs_huerfanos = requerimientos.annotate(
        rel_count=Count('relaciones_casos')
    ).filter(rel_count=0)
    
    casos_huerfanos = casos.annotate(
        rel_count=Count('relaciones_requerimientos')
    ).filter(rel_count=0)
    
    context = {
        'proyecto': proyecto,
        'requerimientos': requerimientos,
        'casos': casos,
        'matriz': matriz,
        'total_requerimientos': total_requerimientos,
        'total_casos': total_casos,
        'total_relaciones': total_relaciones,
        'reqs_con_casos': reqs_con_casos,
        'casos_con_reqs': casos_con_reqs,
        'cobertura_reqs': round(cobertura_reqs, 1),
        'cobertura_casos': round(cobertura_casos, 1),
        'req_por_estado': req_por_estado,
        'req_por_tipo': req_por_tipo,
        'reqs_huerfanos': reqs_huerfanos,
        'casos_huerfanos': casos_huerfanos,
        'es_lider': es_lider,
        'page_title': f'Matriz de Trazabilidad - {proyecto.nombre}',
        # Filtros actuales
        'filtro_tipo_req': tipo_req,
        'filtro_estado_req': estado_req,
        'filtro_solo_huerfanos': solo_huerfanos,
        'filtro_solo_sin_cubrir': solo_sin_cubrir,
    }
    
    return render(request, 'proyectos/matriz_trazabilidad.html', context)


@login_required
def exportar_matriz(request, proyecto_id, formato):
    """
    Exporta la matriz de trazabilidad en diferentes formatos: PDF, Excel, CSV.
    """
    from requerimientos.models import Requerimiento, RequerimientoCaso
    from casos_de_uso.models import CasoDeUso
    from django.http import HttpResponse
    import csv
    from datetime import datetime
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Verificar permisos
    es_lider = proyecto.lider == request.user
    es_participante = proyecto.participantes.filter(id=request.user.id).exists()
    
    if not (es_lider or es_participante):
        messages.error(request, "No tienes permiso para exportar la matriz de este proyecto.")
        return redirect("dashboards:lider_dashboard")
    
    # Obtener datos
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto).prefetch_related(
        'relaciones_casos__caso_de_uso'
    ).order_by('id')
    
    casos = CasoDeUso.objects.filter(proyecto=proyecto).order_by('id')
    
    if formato == 'csv':
        # Exportar a CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="matriz_trazabilidad_{proyecto.nombre}_{datetime.now().strftime("%Y%m%d")}.csv"'
        response.write('\ufeff')  # BOM para UTF-8
        
        writer = csv.writer(response)
        
        # Encabezado
        encabezado = ['Requerimiento', 'Tipo', 'Estado']
        for caso in casos:
            encabezado.append(f'CU-{caso.pk}: {caso.nombre}')
        writer.writerow(encabezado)
        
        # Datos
        for req in requerimientos:
            fila = [
                f'REQ-{req.pk}: {req.nombre}',
                req.get_tipo_display(),  # type: ignore[attr-defined]
                req.get_estado_display()  # type: ignore[attr-defined]
            ]
            
            # Verificar relaciones con cada caso
            casos_relacionados_ids = set(
                req.relaciones_casos.values_list('caso_de_uso_id', flat=True)  # type: ignore[attr-defined]
            )
            
            for caso in casos:
                if caso.pk in casos_relacionados_ids:
                    fila.append('✓')
                else:
                    fila.append('')
            
            writer.writerow(fila)
        
        return response
    
    elif formato == 'excel':
        # Exportar a Excel (requiere openpyxl)
        try:
            from openpyxl import Workbook  # type: ignore[import-untyped]
            from openpyxl.styles import Font, PatternFill, Alignment  # type: ignore[import-untyped]
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Matriz de Trazabilidad"  # type: ignore[union-attr]
            
            # Estilos
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            check_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            
            # Encabezado
            encabezado = ['Requerimiento', 'Tipo', 'Estado']
            for caso in casos:
                encabezado.append(f'CU-{caso.pk}')
            
            ws.append(encabezado)  # type: ignore[union-attr]
            
            # Estilo del encabezado
            for cell in ws[1]:  # type: ignore[index]
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Datos
            for req in requerimientos:
                casos_relacionados_ids = set(
                    req.relaciones_casos.values_list('caso_de_uso_id', flat=True)  # type: ignore[attr-defined]
                )
                
                fila = [
                    f'REQ-{req.pk}: {req.nombre}',
                    req.get_tipo_display(),  # type: ignore[attr-defined]
                    req.get_estado_display()  # type: ignore[attr-defined]
                ]
                
                for caso in casos:
                    if caso.pk in casos_relacionados_ids:
                        fila.append('✓')
                    else:
                        fila.append('')
                
                ws.append(fila)  # type: ignore[union-attr]
                
                # Estilo para checkmarks
                row_num = ws.max_row  # type: ignore[union-attr]
                for col_num in range(4, len(encabezado) + 1):
                    cell = ws.cell(row=row_num, column=col_num)  # type: ignore[union-attr]
                    if cell.value == '✓':
                        cell.fill = check_fill
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Ajustar anchos de columna
            ws.column_dimensions['A'].width = 50  # type: ignore[union-attr, index]
            ws.column_dimensions['B'].width = 15  # type: ignore[union-attr, index]
            ws.column_dimensions['C'].width = 15  # type: ignore[union-attr, index]
            for col_num in range(4, len(encabezado) + 1):
                ws.column_dimensions[chr(64 + col_num)].width = 12  # type: ignore[union-attr, index]
            
            # Guardar en response
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="matriz_trazabilidad_{proyecto.nombre}_{datetime.now().strftime("%Y%m%d")}.xlsx"'
            wb.save(response)
            
            return response
            
        except ImportError:
            messages.error(request, "La exportación a Excel requiere instalar 'openpyxl'. Usa CSV como alternativa.")
            return redirect('proyectos:matriz_trazabilidad', proyecto_id=proyecto_id)
    
    elif formato == 'pdf':
        # Exportar a PDF (requiere reportlab)
        try:
            from reportlab.lib import colors  # type: ignore[import-untyped]
            from reportlab.lib.pagesizes import A4, landscape  # type: ignore[import-untyped]
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer  # type: ignore[import-untyped]
            from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import-untyped]
            from reportlab.lib.units import cm  # type: ignore[import-untyped]
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=1*cm, bottomMargin=1*cm)
            elements = []
            styles = getSampleStyleSheet()
            
            # Título
            title = Paragraph(f"<b>Matriz de Trazabilidad</b><br/>{proyecto.nombre}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.5*cm))
            
            # Construir tabla
            data = []
            
            # Encabezado
            encabezado = ['Requerimiento', 'Tipo', 'Estado']
            for caso in casos:
                encabezado.append(f'CU-{caso.pk}')
            data.append(encabezado)
            
            # Datos
            for req in requerimientos:
                casos_relacionados_ids = set(
                    req.relaciones_casos.values_list('caso_de_uso_id', flat=True)  # type: ignore[attr-defined]
                )
                
                fila = [
                    f'REQ-{req.pk}',
                    req.get_tipo_display(),  # type: ignore[attr-defined]
                    req.get_estado_display()  # type: ignore[attr-defined]
                ]
                
                for caso in casos:
                    if caso.pk in casos_relacionados_ids:
                        fila.append('✓')
                    else:
                        fila.append('')
                
                data.append(fila)
            
            # Crear tabla
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            # Retornar PDF
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="matriz_trazabilidad_{proyecto.nombre}_{datetime.now().strftime("%Y%m%d")}.pdf"'
            
            return response
            
        except ImportError:
            messages.error(request, "La exportación a PDF requiere instalar 'reportlab'. Usa CSV como alternativa.")
            return redirect('proyectos:matriz_trazabilidad', proyecto_id=proyecto_id)
    
    else:
        messages.error(request, "Formato de exportación no válido.")
        return redirect('proyectos:matriz_trazabilidad', proyecto_id=proyecto_id)
