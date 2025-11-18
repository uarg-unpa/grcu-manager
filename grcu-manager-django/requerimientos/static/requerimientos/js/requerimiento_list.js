/**
 * requerimiento_list.js
 * 
 * Funcionalidad de búsqueda y filtrado para la lista de requerimientos.
 * Incluye búsqueda en tiempo real con debounce, filtros por estado y tipo,
 * y navegación con teclado.
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('requerimientosSearchInput');
    const filtroEstado = document.getElementById('filtroEstado');
    const filtroTipo = document.getElementById('filtroTipo');
    const tableBody = document.getElementById('requerimientosTableBody');
    const proyectoId = document.body.dataset.proyectoId || null;
    
    let searchTimeout;
    let isSearching = false;

    /**
     * Busca requerimientos según los criterios de búsqueda y filtros.
     * Realiza una petición AJAX al endpoint de búsqueda y actualiza la tabla.
     * 
     * @async
     * @function buscarRequerimientos
     */
    const buscarRequerimientos = async () => {
        const searchTerm = searchInput.value.trim();
        const estado = filtroEstado.value;
        const tipo = filtroTipo.value;

        if (searchTerm === '' && estado === '' && tipo === '') {
            // Si no hay filtros, recargar la página
            window.location.href = window.location.pathname + (proyectoId ? '?proyecto_id=' + proyectoId : '');
            return;
        }

        isSearching = true;

        try {
            // Construir URL con parámetros
            let url = '/requerimientos/buscar/?';
            if (proyectoId) url += `proyecto_id=${proyectoId}&`;
            if (searchTerm) url += `q=${encodeURIComponent(searchTerm)}&`;
            if (estado) url += `estado=${estado}&`;
            if (tipo) url += `tipo=${tipo}&`;

            const response = await fetch(url);
            const data = await response.json();

            // Limpiar tabla
            tableBody.innerHTML = '';

            if (data.count === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="10" class="text-center alert alert-info">
                            <i class="bi bi-info-circle"></i> No se encontraron requerimientos con los criterios especificados.
                        </td>
                    </tr>
                `;
            } else {
                // Renderizar requerimientos
                data.requerimientos.forEach(req => {
                    const row = crearFilaRequerimiento(req);
                    tableBody.insertAdjacentHTML('beforeend', row);
                });
                
                // Reinicializar tooltips para las nuevas filas
                var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl, {
                        delay: { show: 300, hide: 100 }
                    });
                });
            }
        } catch (error) {
            console.error('Error en búsqueda:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="10" class="text-center alert alert-danger">
                        <i class="bi bi-exclamation-triangle"></i> Error al buscar requerimientos. Intenta de nuevo.
                    </td>
                </tr>
            `;
        } finally {
            isSearching = false;
        }
    };

    /**
     * Crea el HTML de una fila de la tabla para un requerimiento.
     * 
     * @param {Object} req - Objeto con los datos del requerimiento
     * @returns {string} HTML de la fila
     */
    function crearFilaRequerimiento(req) {
        // Determinar clase de fila según estado
        const estadoClass = `estado-${req.estado.toLowerCase()}`;
        
        // Badge de estado
        let estadoBadge = '';
        if (req.estado === 'BORRADOR') {
            estadoBadge = `<span class="badge badge-estado-borrador"><i class="bi bi-file-earmark-text me-1"></i>${req.estado_display}</span>`;
        } else if (req.estado === 'VALIDADO') {
            estadoBadge = `<span class="badge bg-info"><i class="bi bi-check-circle-fill me-1"></i>${req.estado_display}</span>`;
        } else if (req.estado === 'PRIORIZADO') {
            estadoBadge = `<span class="badge bg-success"><i class="bi bi-flag-fill me-1"></i>${req.estado_display}</span>`;
        } else if (req.estado === 'EN_PROCESO') {
            estadoBadge = `<span class="badge bg-secondary"><i class="bi bi-gear-fill me-1"></i>${req.estado_display}</span>`;
        } else if (req.estado === 'TERMINADO') {
            estadoBadge = `<span class="badge bg-success"><i class="bi bi-check-circle-fill me-1"></i>${req.estado_display} ✓</span>`;
        } else {
            estadoBadge = `<span class="badge bg-light text-dark">${req.estado_display}</span>`;
        }
        
        // Badge de prioridad
        let prioridadHtml = '';
        if (req.prioridad) {
            if (req.prioridad === 'MUST') {
                prioridadHtml = `<span class="badge" style="background-color: #4A90E2; color: white; font-weight: bold;">
                    <i class="bi bi-exclamation-circle-fill"></i> Crítico (Must)
                </span>`;
            } else if (req.prioridad === 'SHOULD') {
                prioridadHtml = `<span class="badge" style="background-color: #9B59B6; color: white; font-weight: bold;">
                    <i class="bi bi-star-fill"></i> Importante (Should)
                </span>`;
            } else if (req.prioridad === 'COULD') {
                prioridadHtml = `<span class="badge" style="background-color: #5DADE2; color: white; font-weight: bold;">
                    <i class="bi bi-check-circle"></i> Deseable (Could)
                </span>`;
            } else if (req.prioridad === 'WONT') {
                prioridadHtml = `<span class="badge" style="background-color: #95A5A6; color: white; font-weight: bold;">
                    <i class="bi bi-x-circle"></i> Descartado (Won't)
                </span>`;
            }
        } else {
            prioridadHtml = `<span class="text-muted small"><i class="bi bi-dash-circle"></i> Sin prioridad</span>`;
        }
        
        // Dependencias
        let dependenciasHtml = '';
        if (req.dependencias && req.dependencias.length > 0) {
            dependenciasHtml = '<div class="d-flex flex-column gap-1">';
            req.dependencias.forEach(dep => {
                const depClass = `badge-dep-${dep.estado.toLowerCase()}`;
                dependenciasHtml += `
                    <a href="/requerimientos/${dep.id}/" 
                       class="badge ${depClass} text-decoration-none"
                       data-bs-toggle="tooltip" 
                       data-bs-placement="left"
                       title="Depende de: ${dep.nombre} (${dep.estado_display})">
                        <i class="bi bi-arrow-left-circle me-1"></i>${dep.nombre.substring(0, 20)}${dep.nombre.length > 20 ? '...' : ''}
                    </a>`;
            });
            dependenciasHtml += '</div>';
        } else {
            dependenciasHtml = `<span class="text-muted small"><i class="bi bi-dash-circle"></i> Sin dependencias</span>`;
        }
        
        // Comentarios
        let comentariosHtml = '';
        if (req.num_comentarios > 0) {
            comentariosHtml = `
                <a href="/requerimientos/${req.id}/discusion/" 
                   class="comentarios-badge-link"
                   data-bs-toggle="tooltip" 
                   data-bs-placement="top"
                   title="Ver ${req.num_comentarios} comentario${req.num_comentarios > 1 ? 's' : ''}">
                    <span class="badge comentarios-badge comentarios-pulse">
                        <i class="bi bi-chat-dots-fill"></i>
                        <span class="comentarios-count">${req.num_comentarios}</span>
                    </span>
                </a>`;
        } else {
            comentariosHtml = `<span class="text-muted small"><i class="bi bi-chat"></i> Sin comentarios</span>`;
        }
        
        // Casos de uso
        const casosHtml = req.casos.length === 0
            ? '<span class="badge badge-huerfano"><i class="bi bi-exclamation-triangle me-1"></i>Huérfano</span>'
            : req.casos.map(caso => 
                `<a href="/casos-de-uso/${caso.id}/" class="badge badge-caso-uso me-1"><i class="bi bi-diagram-3 me-1"></i>${caso.nombre}</a>`
              ).join('');
        
        // Obtener el ID del usuario actual y roles desde el dataset del body (si está disponible)
        const currentUserId = document.body.dataset.userId || null;
        const isLider = document.body.dataset.isLider === 'true';
        const isStakeholder = document.body.dataset.isStakeholder === 'true';
        
        // Botones de acción
        let accionesHtml = `
            <div class="d-flex gap-1 flex-wrap">
                <a href="/requerimientos/${req.id}/" 
                   class="btn btn-outline-success btn-sm btn-action-req" 
                   title="Ver Detalle">
                    <i class="bi bi-eye"></i>
                </a>`;
        
        // Botón editar (solo para líder o creador)
        if (currentUserId && (currentUserId == req.proyecto_lider_id || currentUserId == req.creado_por_id)) {
            accionesHtml += `
                <a href="/requerimientos/${req.id}/editar/" 
                   class="btn btn-outline-warning btn-sm btn-action-req" 
                   title="Editar">
                    <i class="bi bi-pencil"></i>
                </a>`;
        }
        
        // Botón eliminar (solo para líder)
        if (currentUserId && currentUserId == req.proyecto_lider_id) {
            accionesHtml += `
                <a href="/requerimientos/${req.id}/eliminar/" 
                   class="btn btn-outline-danger btn-sm btn-action-req" 
                   title="Eliminar">
                    <i class="bi bi-trash"></i>
                </a>`;
        }
        
        // Botones de validación para requerimientos BORRADOR
        if (req.estado === 'BORRADOR') {
            if (isLider) {
                accionesHtml += `
                    <a href="/requerimientos/${req.id}/validar-lider-individual/" 
                       class="btn btn-validar-lider btn-sm btn-action-req" 
                       title="Validar como líder">
                        <i class="bi bi-check-circle-fill"></i> Validar
                    </a>`;
            }
            
            if (isStakeholder) {
                accionesHtml += `
                    <a href="/requerimientos/${req.id}/validar-cliente-individual/" 
                       class="btn btn-validar-stakeholder btn-sm btn-action-req" 
                       title="Validar como stakeholder">
                        <i class="bi bi-person-check-fill"></i> Validar
                    </a>`;
            }
        }
        
        // Botones de aprobación para stakeholders cuando el requerimiento está VALIDADO
        if (req.estado === 'VALIDADO' && isStakeholder) {
            accionesHtml += `
                <a href="/requerimientos/${req.id}/validar-cliente-individual/" 
                   class="btn btn-success btn-sm btn-action-req" 
                   title="Aprobar como cliente">
                    <i class="bi bi-clipboard-check-fill"></i> Aprobar
                </a>`;
        }
        
        // Solo mostrar botones de casos de uso para requerimientos FUNCIONALES que NO estén en BORRADOR
        if (req.tipo === 'FUNCIONAL' && req.estado !== 'BORRADOR') {
            if (req.casos.length === 0) {
                // Sin casos de uso asociados
                accionesHtml += `
                    <a href="/casos-de-uso/crear-con-requerimiento/${req.proyecto_id}/${req.id}/" 
                       class="btn btn-outline-primary btn-sm btn-action-req" 
                       title="Crear Caso de Uso">
                        <i class="bi bi-diagram-3-fill"></i>
                    </a>
                    <a href="/requerimientos/${req.id}/relacionar-casos/" 
                       class="btn btn-outline-secondary btn-sm btn-action-req" 
                       title="Relacionar Caso de Uso Existente">
                        <i class="bi bi-link"></i>
                    </a>`;
            } else {
                // Ya tiene casos de uso, permitir agregar más
                accionesHtml += `
                    <a href="/casos-de-uso/crear-con-requerimiento/${req.proyecto_id}/${req.id}/" 
                       class="btn btn-outline-info btn-sm btn-action-req" 
                       title="Agregar Otro Caso de Uso">
                        <i class="bi bi-plus-circle"></i>
                    </a>
                    <a href="/requerimientos/${req.id}/relacionar-casos/" 
                       class="btn btn-outline-secondary btn-sm btn-action-req" 
                       title="Relacionar Caso de Uso Existente">
                        <i class="bi bi-link"></i>
                    </a>`;
            }
        }
        
        accionesHtml += `</div>`;

        return `
            <tr class="requerimiento-row ${estadoClass}">
                <td>
                    <a href="/requerimientos/${req.id}/" 
                       class="fw-bold text-decoration-none req-tooltip"
                       data-bs-toggle="tooltip" 
                       data-bs-placement="right"
                       data-bs-html="true"
                       title="<strong>${req.nombre}</strong><br>
                              <small><strong>Tipo:</strong> ${req.tipo_display}</small><br>
                              <small><strong>Estado:</strong> ${req.estado_display}</small><br>
                              <small><strong>Creado:</strong> ${req.fecha_creacion}</small>">
                        ${req.nombre}
                    </a>
                </td>
                <td>${req.tipo_display}</td>
                <td>${estadoBadge}</td>
                <td>${prioridadHtml}</td>
                <td>${dependenciasHtml}</td>
                <td class="text-center">${comentariosHtml}</td>
                <td class="small text-muted">${req.descripcion || '-'}</td>
                <td>${req.fecha_creacion}</td>
                <td>${casosHtml}</td>
                <td>${accionesHtml}</td>
            </tr>
        `;
    }

    // Event listener para búsqueda con debounce
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            if (isSearching) return;
            
            searchTimeout = setTimeout(() => {
                buscarRequerimientos();
            }, 300);
        });

        // Atajos de teclado
        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                // ESC: Limpiar búsqueda y filtros
                this.value = '';
                filtroEstado.value = '';
                filtroTipo.value = '';
                clearTimeout(searchTimeout);
                window.location.href = window.location.pathname + (proyectoId ? '?proyecto_id=' + proyectoId : '');
            }
            if (event.key === 'Enter') {
                // ENTER: Buscar inmediatamente
                event.preventDefault();
                clearTimeout(searchTimeout);
                buscarRequerimientos();
            }
        });
    }

    // Event listeners para filtros
    if (filtroEstado) {
        filtroEstado.addEventListener('change', buscarRequerimientos);
    }

    if (filtroTipo) {
        filtroTipo.addEventListener('change', buscarRequerimientos);
    }
});
