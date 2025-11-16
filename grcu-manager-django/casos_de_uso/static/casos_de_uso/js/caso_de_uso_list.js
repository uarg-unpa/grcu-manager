/**
 * CASOS DE USO - Lista y Búsqueda v2.0
 * Funcionalidad mejorada para buscar y filtrar casos de uso
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('casosSearchInput');
    const table = document.getElementById('casosTable');
    const rows = table ? table.querySelectorAll('tbody tr') : [];
    
    // Obtener proyecto ID desde el data attribute del body o elemento contenedor
    const proyectoId = document.body.dataset.proyectoId || null;
    
    let searchTimeout;

    /**
     * Función para filtrar casos de uso en tiempo real (sin AJAX)
     * Filtra por nombre, descripción, requerimiento y proyecto
     */
    const filtrarCasos = () => {
        const searchTerm = searchInput.value.toLowerCase().trim();

        let visibleCount = 0;

        rows.forEach(row => {
            // Saltar fila vacía
            if (row.querySelector('.empty-state-caso')) {
                row.style.display = 'none';
                return;
            }

            const nombre = row.cells[0]?.textContent.toLowerCase() || '';
            const requerimiento = row.cells[1]?.textContent.toLowerCase() || '';
            const proyecto = row.cells[2]?.textContent.toLowerCase() || '';
            const descripcion = row.cells[4]?.textContent.toLowerCase() || '';
            const creador = row.cells[3]?.getAttribute('title')?.toLowerCase() || '';

            const matches = nombre.includes(searchTerm) || 
                          descripcion.includes(searchTerm) ||
                          requerimiento.includes(searchTerm) ||
                          proyecto.includes(searchTerm) ||
                          creador.includes(searchTerm);

            if (matches) {
                row.style.display = '';
                visibleCount++;
                
                // Resaltar término de búsqueda
                if (searchTerm) {
                    row.classList.add('search-highlight');
                } else {
                    row.classList.remove('search-highlight');
                }
            } else {
                row.style.display = 'none';
                row.classList.remove('search-highlight');
            }
        });

        // Mostrar mensaje si no hay resultados
        const tbody = table.querySelector('tbody');
        let noResultsRow = tbody.querySelector('.no-results-row');
        
        if (visibleCount === 0 && searchTerm) {
            if (!noResultsRow) {
                noResultsRow = document.createElement('tr');
                noResultsRow.className = 'no-results-row';
                noResultsRow.innerHTML = `
                    <td colspan="7">
                        <div class="empty-state-caso">
                            <i class="bi bi-search"></i>
                            <p class="mb-0">No se encontraron casos de uso que coincidan con "<strong>${searchTerm}</strong>"</p>
                            <button class="btn btn-sm btn-outline-secondary mt-2" onclick="document.getElementById('casosSearchInput').value = ''; document.getElementById('casosSearchInput').dispatchEvent(new Event('input'));">
                                <i class="bi bi-x-circle me-1"></i>Limpiar búsqueda
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(noResultsRow);
            }
        } else if (noResultsRow) {
            noResultsRow.remove();
        }

        // Actualizar contador si existe
        updateResultCount(visibleCount, rows.length - 1); // -1 para excluir empty state
    };

    /**
     * Actualizar contador de resultados
     */
    const updateResultCount = (visible, total) => {
        let counter = document.getElementById('casosCounter');
        if (!counter) {
            counter = document.createElement('div');
            counter.id = 'casosCounter';
            counter.className = 'text-muted small mb-2';
            const card = document.querySelector('.casos-uso-list-card');
            if (card) {
                card.insertBefore(counter, card.firstChild);
            }
        }
        
        if (searchInput.value.trim()) {
            counter.innerHTML = `<i class="bi bi-filter-circle me-1"></i>Mostrando <strong>${visible}</strong> de <strong>${total}</strong> casos de uso`;
            counter.style.display = 'block';
            counter.style.padding = '10px 15px';
            counter.style.backgroundColor = '#f8f9fa';
            counter.style.borderBottom = '1px solid #dee2e6';
        } else {
            counter.style.display = 'none';
        }
    };

    /**
     * Event listener para búsqueda con debounce
     * Espera 300ms después de la última tecla antes de filtrar
     */
    if (searchInput && table) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                filtrarCasos();
            }, 150);
        });

        // Atajos de teclado
        searchInput.addEventListener('keydown', function(event) {
            // ESC: Limpiar búsqueda
            if (event.key === 'Escape') {
                this.value = '';
                clearTimeout(searchTimeout);
                filtrarCasos();
            }
            
            // ENTER: Filtrar inmediatamente
            if (event.key === 'Enter') {
                event.preventDefault();
                clearTimeout(searchTimeout);
                filtrarCasos();
            }
        });

        // Focus en búsqueda con Ctrl/Cmd + K
        document.addEventListener('keydown', function(event) {
            if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
                event.preventDefault();
                searchInput.focus();
                searchInput.select();
            }
        });
    }

    // Animar entrada de filas
    rows.forEach((row, index) => {
        if (!row.querySelector('.empty-state-caso')) {
            row.style.opacity = '0';
            row.style.transform = 'translateY(10px)';
            setTimeout(() => {
                row.style.transition = 'all 0.3s ease';
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, index * 30);
        }
    });
});

// Agregar estilos para resaltado de búsqueda
const style = document.createElement('style');
style.textContent = `
    .search-highlight {
        animation: highlight-pulse 0.5s ease-in-out;
    }
    
    @keyframes highlight-pulse {
        0% { background-color: inherit; }
        50% { background-color: rgba(59, 130, 246, 0.1); }
        100% { background-color: inherit; }
    }
`;
document.head.appendChild(style);

