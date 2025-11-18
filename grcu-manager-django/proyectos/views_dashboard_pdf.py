"""
Vista para exportar el dashboard del proyecto a PDF
"""
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from proyectos.models import Proyecto
from requerimientos.models import Requerimiento, RequerimientoCaso
from casos_de_uso.models import CasoDeUso
from django.db.models import Count
from datetime import datetime
import os
from django.conf import settings

def is_admin(user):
    return hasattr(user, 'es_admin') and user.es_admin()


@login_required
@user_passes_test(is_admin)
def exportar_dashboard_pdf(request, proyecto_id):
    """
    Genera un PDF con la información del dashboard del proyecto.
    Incluye métricas, integrantes, clientes, requerimientos y casos de uso.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from io import BytesIO
    except ImportError:
        from django.contrib import messages
        messages.error(request, "La exportación a PDF requiere instalar 'reportlab'.")
        from django.shortcuts import redirect
        return redirect('proyectos:proyecto_detail_admin', proyecto_id=proyecto_id)
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener datos del proyecto
    requerimientos = Requerimiento.objects.filter(proyecto=proyecto)
    casos = CasoDeUso.objects.filter(proyecto=proyecto)
    integrantes = list(proyecto.participantes.all())
    clientes = list(proyecto.clientes.all())
    
    # Métricas
    req_estado_qs = requerimientos.values('estado').annotate(count=Count('id'))
    req_estado_map = {item['estado']: item['count'] for item in req_estado_qs}
    
    req_tipo_qs = requerimientos.values('tipo').annotate(count=Count('id'))
    req_tipo_map = {item['tipo']: item['count'] for item in req_tipo_qs}
    
    # Huérfanos
    reqs_huerfanos = requerimientos.annotate(rel_count=Count('relaciones_casos')).filter(rel_count=0)
    casos_huerfanos = casos.annotate(rel_count=Count('relaciones_requerimientos')).filter(rel_count=0)
    
    # Crear buffer y documento PDF
    buffer = BytesIO()
    
    # Preparar paths de logos
    logo_proyecto_path = None
    if proyecto.logo:
        logo_proyecto_path = os.path.join(settings.MEDIA_ROOT, str(proyecto.logo))
        if not os.path.exists(logo_proyecto_path):
            logo_proyecto_path = None
    
    logo_grupo_path = None
    if proyecto.grupo and proyecto.grupo.logo:
        logo_grupo_path = os.path.join(settings.MEDIA_ROOT, str(proyecto.grupo.logo))
        if not os.path.exists(logo_grupo_path):
            logo_grupo_path = None
    
    # Importar la función de header/footer
    from proyectos.views import crear_header_footer
    
    # Crear documento con márgenes
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm,
        title=f"Dashboard - {proyecto.nombre}"
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=0.3*cm,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=0.2*cm,
        spaceBefore=0.4*cm,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=0.1*cm
    )
    
    # Contenido del PDF
    story = []
    
    # === TÍTULO ===
    story.append(Paragraph(f"Dashboard del Proyecto", titulo_style))
    # Usar Paragraph para manejar texto largo automáticamente
    proyecto_titulo = proyecto.nombre if len(proyecto.nombre) <= 60 else proyecto.nombre[:60] + '...'
    story.append(Paragraph(proyecto_titulo, titulo_style))
    story.append(Spacer(1, 0.5*cm))
    
    # === INFORMACIÓN GENERAL ===
    story.append(Paragraph("Información General", subtitulo_style))
    
    # Estilo para celdas de tabla
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        wordWrap='CJK'
    )
    
    # Truncar descripción si es muy larga
    descripcion = proyecto.descripcion or 'Sin descripción'
    if len(descripcion) > 200:
        descripcion = descripcion[:200] + '...'
    
    info_data = [
        ['Descripción:', Paragraph(descripcion, cell_style)],
        ['Metodología:', proyecto.get_metodologia_display() if proyecto.metodologia else 'No asignada'],
        ['Grupo:', Paragraph(proyecto.grupo.nombre if proyecto.grupo else 'Sin grupo asignado', cell_style)],
        ['Líder:', proyecto.lider.nombre if proyecto.lider else 'No asignado'],
        ['Estado:', 'Activo' if proyecto.activo else 'Inactivo'],
        ['Fecha de creación:', proyecto.fecha_creacion.strftime('%d/%m/%Y')],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*cm))
    
    # === MÉTRICAS DE REQUERIMIENTOS ===
    story.append(Paragraph("Métricas de Requerimientos", subtitulo_style))
    
    metricas_data = [
        ['Total de Requerimientos:', str(requerimientos.count())],
        ['', ''],
        ['Por Estado:', ''],
        ['  • Borrador:', str(req_estado_map.get('BORRADOR', 0))],
        ['  • Validado:', str(req_estado_map.get('VALIDADO', 0))],
        ['  • Priorizado:', str(req_estado_map.get('PRIORIZADO', 0))],
        ['  • En Proceso:', str(req_estado_map.get('EN_PROCESO', 0))],
        ['  • Terminado:', str(req_estado_map.get('TERMINADO', 0))],
        ['', ''],
        ['Por Tipo:', ''],
        ['  • Funcional:', str(req_tipo_map.get('FUNCIONAL', 0))],
        ['  • No Funcional:', str(req_tipo_map.get('NO_FUNCIONAL', 0))],
        ['  • Sistema:', str(req_tipo_map.get('SISTEMA', 0))],
        ['', ''],
        ['Huérfanos:', str(reqs_huerfanos.count())],
    ]
    
    metricas_table = Table(metricas_data, colWidths=[10*cm, 6*cm])
    metricas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(metricas_table)
    story.append(Spacer(1, 0.5*cm))
    
    # === CASOS DE USO ===
    story.append(Paragraph("Casos de Uso", subtitulo_style))
    
    casos_data = [
        ['Total de Casos de Uso:', str(casos.count())],
        ['Casos Huérfanos:', str(casos_huerfanos.count())],
    ]
    
    casos_table = Table(casos_data, colWidths=[10*cm, 6*cm])
    casos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(casos_table)
    story.append(Spacer(1, 0.5*cm))
    
    # === INTEGRANTES ===
    if integrantes:
        story.append(Paragraph(f"Integrantes del Equipo ({len(integrantes)})", subtitulo_style))
        
        integrantes_data = [['Nombre', 'Email', 'Rol']]
        for i in integrantes:
            rol_names = ', '.join([r.nombre for r in i.roles.all()]) if i.roles.exists() else 'Sin rol'
            # Truncar email si es muy largo
            email_display = i.email if len(i.email) <= 30 else i.email[:27] + '...'
            integrantes_data.append([
                Paragraph(i.nombre, cell_style),
                Paragraph(email_display, cell_style),
                Paragraph(rol_names, cell_style)
            ])
        
        integrantes_table = Table(integrantes_data, colWidths=[5*cm, 6.5*cm, 4.5*cm])
        integrantes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(integrantes_table)
        story.append(Spacer(1, 0.5*cm))
    
    # === CLIENTES ===
    if clientes:
        story.append(Paragraph(f"Clientes/Stakeholders ({len(clientes)})", subtitulo_style))
        
        clientes_data = [['Nombre', 'Email']]
        for c in clientes:
            # Truncar email si es muy largo
            email_display = c.email if len(c.email) <= 35 else c.email[:32] + '...'
            clientes_data.append([
                Paragraph(c.nombre, cell_style),
                Paragraph(email_display, cell_style)
            ])
        
        clientes_table = Table(clientes_data, colWidths=[7*cm, 9*cm])
        clientes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(clientes_table)
    
    # Construir PDF con header/footer personalizado
    def add_header_footer(canvas, doc):
        crear_header_footer(canvas, doc, proyecto, logo_proyecto_path, logo_grupo_path, total_pages=0)
    
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    # Retornar PDF
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="dashboard_{proyecto.nombre.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response
