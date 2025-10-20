/**
 * CASOS DE USO - Lista y Búsqueda
 * Funcionalidad para buscar y filtrar casos de uso
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('casosSearchInput');
    const filtroTipoDetalle = document.getElementById('filtroTipoDetalle');
    const tableBody = document.querySelector('.casos-uso-list-card tbody');
    
    // Obtener proyecto ID desde el data attribute del body o elemento contenedor
    const proyectoId = document.body.dataset.proyectoId || null;
    
    let searchTimeout;
    let isSearching = false;

    /**
     * Función para buscar casos de uso
     * Realiza una petición AJAX al endpoint de búsqueda
     */
    const buscarCasos = async () => {
        const searchTerm = searchInput.value.trim();
        const tipoDetalle = filtroTipoDetalle.value;

        // Si no hay filtros, recargar la página
        if (searchTerm === '' && tipoDetalle === '') {
            window.location.href = window.location.pathname + (proyectoId ? '?proyecto_id=' + proyectoId : '');
            return;
        }

        isSearching = true;

        try {
            // Construir URL con parámetros
            let url = '/casos-de-uso/buscar/?';
            if (proyectoId) url += `proyecto_id=${proyectoId}&`;
            if (searchTerm) url += `q=${encodeURIComponent(searchTerm)}&`;
            if (tipoDetalle) url += `tipo_detalle=${tipoDetalle}&`;

            const response = await fetch(url);
            const data = await response.json();

            // Limpiar tabla
            tableBody.innerHTML = '';

            if (data.count === 0) {
                // No se encontraron resultados
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5">
                            <div class="empty-state-caso">
                                <i class="bi bi-inbox"></i>
                                <p class="mb-0">No se encontraron casos de uso con los criterios especificados.</p>
                            </div>
                        </td>
                    </tr>
                `;
            } else {
                // Renderizar casos de uso encontrados
                data.casos.forEach(caso => {
                    const row = crearFilaCasoUso(caso);
                    tableBody.insertAdjacentHTML('beforeend', row);
                });
            }
        } catch (error) {
            console.error('Error en búsqueda:', error);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5">
                        <div class="alert alert-danger mb-0 text-center">
                            <i class="bi bi-exclamation-triangle me-2"></i>
                            Error al buscar casos de uso. Intenta de nuevo.
                        </div>
                    </td>
                </tr>
            `;
        } finally {
            isSearching = false;
        }
    };

    /**
     * Crea el HTML de una fila de caso de uso
     * @param {Object} caso - Objeto con datos del caso de uso
     * @returns {string} HTML de la fila
     */
    const crearFilaCasoUso = (caso) => {
        // Determinar badge de tipo
        let tipoBadge = '<span class="badge bg-secondary">Sin tipo</span>';
        if (caso.tipo === 'tradicional') {
            tipoBadge = '<span class="badge badge-tradicional"><i class="bi bi-book me-1"></i>Tradicional</span>';
        } else if (caso.tipo === 'agil') {
            tipoBadge = '<span class="badge badge-agil"><i class="bi bi-lightning me-1"></i>Ágil</span>';
        }

        return `
            <tr>
                <td>${caso.id}</td>
                <td>${caso.nombre}</td>
                <td>${tipoBadge}</td>
                <td>${caso.descripcion || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info btn-action-caso btn-toggle-detalle" 
                            type="button" 
                            data-bs-toggle="collapse" 
                            data-bs-target="#detalle-${caso.id}" 
                            title="Ver Detalles">
                        <i class="bi bi-chevron-down"></i>
                    </button>
                    <a href="/casos-de-uso/${caso.id}/" 
                       class="btn btn-sm btn-outline-info btn-action-caso" 
                       title="Ver Completo">
                        <i class="bi bi-eye"></i>
                    </a>
                </td>
            </tr>
        `;
    };

    /**
     * Event listener para búsqueda con debounce
     * Espera 300ms después de la última tecla antes de buscar
     */
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            if (isSearching) return;
            
            searchTimeout = setTimeout(() => {
                buscarCasos();
            }, 300);
        });

        // Atajos de teclado
        searchInput.addEventListener('keydown', function(event) {
            // ESC: Limpiar búsqueda y recargar
            if (event.key === 'Escape') {
                this.value = '';
                filtroTipoDetalle.value = '';
                clearTimeout(searchTimeout);
                window.location.href = window.location.pathname + (proyectoId ? '?proyecto_id=' + proyectoId : '');
            }
            
            // ENTER: Buscar inmediatamente
            if (event.key === 'Enter') {
                event.preventDefault();
                clearTimeout(searchTimeout);
                buscarCasos();
            }
        });
    }

    /**
     * Event listener para filtro de tipo
     * Busca inmediatamente al cambiar el select
     */
    if (filtroTipoDetalle) {
        filtroTipoDetalle.addEventListener('change', buscarCasos);
    }
});
