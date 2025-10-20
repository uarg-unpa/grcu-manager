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
                        <td colspan="7" class="text-center alert alert-info">
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
            }
        } catch (error) {
            console.error('Error en búsqueda:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center alert alert-danger">
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
        const casosHtml = req.casos.length === 0
            ? '<span class="badge badge-huerfano"><i class="bi bi-exclamation-triangle me-1"></i>Huérfano</span>'
            : req.casos.map(caso => 
                `<a href="/casos-de-uso/${caso.id}/" class="badge badge-caso-uso me-1"><i class="bi bi-diagram-3 me-1"></i>${caso.nombre}</a>`
              ).join('');

        return `
            <tr>
                <td>
                    <a href="/requerimientos/${req.id}/" class="fw-bold text-decoration-none">
                        ${req.nombre}
                    </a>
                </td>
                <td>${req.tipo_display}</td>
                <td>${req.estado_display}</td>
                <td>${req.descripcion || '-'}</td>
                <td>${req.fecha_creacion}</td>
                <td>${casosHtml}</td>
                <td>
                    <a href="/requerimientos/${req.id}/" class="btn btn-outline-success btn-sm btn-action-req" title="Ver Detalle">
                        <i class="bi bi-eye"></i>
                    </a>
                </td>
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
