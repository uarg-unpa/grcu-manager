/**
 * CASOS DE USO - Lista y Búsqueda
 * Funcionalidad para buscar y filtrar casos de uso
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('casosSearchInput');
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

        // Si no hay filtros, recargar la página
        if (searchTerm === '') {
            window.location.href = window.location.pathname + (proyectoId ? '?proyecto_id=' + proyectoId : '');
            return;
        }

        isSearching = true;

        try {
            // Construir URL con parámetros
            let url = '/casos-de-uso/buscar/?';
            if (proyectoId) url += `proyecto_id=${proyectoId}&`;
            if (searchTerm) url += `q=${encodeURIComponent(searchTerm)}&`;

            const response = await fetch(url);
            const data = await response.json();

            // Limpiar tabla
            tableBody.innerHTML = '';

            if (data.count === 0) {
                // No se encontraron resultados
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4">
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
                    <td colspan="4">
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

    const crearFilaCasoUso = (caso) => {
        return `
            <tr>
                <td>${caso.id}</td>
                <td>${caso.nombre}</td>
                <td>${caso.descripcion || '-'}</td>
                <td>
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
});
