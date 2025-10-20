document.addEventListener('DOMContentLoaded', function(){
    // 🔍 Búsqueda con AJAX (del lado del servidor)
    const searchInput = document.getElementById('usuariosSearchInput');
    const usuariosTableBody = document.getElementById('usuariosTableBody');
    let searchTimeout;
    let isSearching = false;

    const searchUsuarios = async (searchTerm) => {
        if (searchTerm.trim() === '') {
            // Si está vacío, recargar la página para mostrar todos
            window.location.href = window.location.pathname;
            return;
        }

        isSearching = true;

        try {
            const response = await fetch(`/usuarios/buscar/?q=${encodeURIComponent(searchTerm)}`);
            const data = await response.json();

            // Limpiar tabla
            usuariosTableBody.innerHTML = '';

            if (data.count === 0) {
                // No hay resultados
                usuariosTableBody.innerHTML = `
                    <tr class="no-results-message">
                        <td colspan="7" class="text-center alert alert-info">
                            <i class="bi bi-info-circle"></i> No se encontraron usuarios que coincidan con "${searchTerm}".
                        </td>
                    </tr>
                `;
            } else {
                // Renderizar usuarios encontrados
                data.usuarios.forEach(usuario => {
                    const avatarHtml = usuario.avatar 
                        ? `<img src="${usuario.avatar}" alt="Avatar" class="usuario-lista-avatar">`
                        : `<i class="bi bi-person-circle usuario-lista-avatar-fallback"></i>`;

                    const activeIcon = usuario.is_active
                        ? '<i class="bi bi-check-circle-fill text-success"></i>'
                        : '<i class="bi bi-x-circle-fill text-danger"></i>';

                    const rolesHtml = usuario.roles.length > 0
                        ? usuario.roles.map(rol => `<span class="usuario-lista-rol">${rol}</span>`).join(' ')
                        : '<span class="text-muted">Sin rol</span>';

                    const row = `
                        <tr data-user-id="${usuario.id}">
                            <td><input type="checkbox" class="row-checkbox" value="${usuario.id}"></td>
                            <td class="usuario-lista-avatar-cell">${avatarHtml}</td>
                            <td class="text-center">${activeIcon}</td>
                            <td>${usuario.nombre}</td>
                            <td>${usuario.email}</td>
                            <td>${rolesHtml}</td>
                            <td>
                                <a href="/usuarios/editar/${usuario.id}/" class="usuario-lista-btn-warning" title="Editar" data-bs-toggle="tooltip">
                                    <i class="bi bi-pencil"></i>
                                </a>
                                <a href="/usuarios/eliminar/${usuario.id}/" class="usuario-lista-btn-danger" title="Eliminar" data-bs-toggle="tooltip">
                                    <i class="bi bi-trash"></i>
                                </a>
                            </td>
                        </tr>
                    `;
                    usuariosTableBody.insertAdjacentHTML('beforeend', row);
                });

                // Reinicializar checkboxes después de agregar nuevas filas
                initializeCheckboxes();
            }
        } catch (error) {
            console.error('Error en búsqueda AJAX:', error);
            usuariosTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center alert alert-danger">
                        <i class="bi bi-exclamation-triangle"></i> Error al buscar usuarios. Por favor, intenta de nuevo.
                    </td>
                </tr>
            `;
        } finally {
            isSearching = false;
        }
    };

    // Event listeners para la búsqueda con debounce
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.trim();
            
            clearTimeout(searchTimeout);
            
            // Si está buscando actualmente, esperar
            if (isSearching) return;

            // Debounce de 300ms (más rápido y responsivo)
            searchTimeout = setTimeout(() => {
                searchUsuarios(searchTerm);
            }, 300);
        });

        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                this.value = '';
                clearTimeout(searchTimeout);
                window.location.href = window.location.pathname;
            }
            if (event.key === 'Enter') {
                event.preventDefault();
                clearTimeout(searchTimeout);
                searchUsuarios(this.value.trim());
            }
        });
    }

    // Función para inicializar checkboxes
    function initializeCheckboxes() {
        const selectAll = document.getElementById('selectAllUsers');
        const checkboxes = Array.from(document.querySelectorAll('.row-checkbox'));
        
        if(selectAll){
            // Limpiar listeners previos
            const newSelectAll = selectAll.cloneNode(true);
            selectAll.parentNode.replaceChild(newSelectAll, selectAll);
            
            newSelectAll.addEventListener('change', function(){
                checkboxes.forEach(cb => {
                    cb.checked = newSelectAll.checked;
                    const tr = cb.closest('tr');
                    tr.classList.toggle('selected', cb.checked);
                });
            });
        }
        
        checkboxes.forEach(cb => {
            cb.addEventListener('change', function(){
                const tr = cb.closest('tr');
                tr.classList.toggle('selected', cb.checked);
            });
        });
    }

    // Inicializar checkboxes al cargar la página
    initializeCheckboxes();
});