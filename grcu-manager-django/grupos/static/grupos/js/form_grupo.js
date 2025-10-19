document.addEventListener('DOMContentLoaded', function() {
    // Función para manejar los badges de integrantes
    const setBadgeState = (badge, isChecked) => {
        badge.classList.toggle('active', isChecked);
        badge.classList.toggle('inactive', !isChecked);
        badge.setAttribute('aria-checked', isChecked);
    };

    // Función para actualizar el campo hidden con los IDs seleccionados
    const updateIntegrantesField = () => {
        const selectedIds = [];
        document.querySelectorAll('.roles-badge input[type="checkbox"]:checked').forEach(cb => {
            selectedIds.push(cb.value);
        });
        // Actualizar campo oculto con IDs únicos
        const uniqueIds = [...new Set(selectedIds)]; // Eliminar duplicados
        document.getElementById('integrantes_seleccionados').value = JSON.stringify(uniqueIds);
        updateIntegrantesSeleccionados();
    };

    // Función para actualizar la sección de integrantes seleccionados
    const updateIntegrantesSeleccionados = () => {
        const seleccionadosContainer = document.getElementById('integrantes-seleccionados');
        const selectedCheckboxes = document.querySelectorAll('.roles-badge input[type="checkbox"]:checked');

        // Limpiar contenedor
        seleccionadosContainer.innerHTML = '';

        if (selectedCheckboxes.length === 0) {
            // Mostrar mensaje cuando no hay seleccionados
            const emptyMessage = document.querySelector('.text-muted');
            if (emptyMessage) {
                emptyMessage.style.display = 'block';
            }
            return;
        }

        // Ocultar mensaje vacío
        const emptyMessage = document.querySelector('.text-muted');
        if (emptyMessage) {
            emptyMessage.style.display = 'none';
        }

        // Agregar cada integrante seleccionado
        selectedCheckboxes.forEach(checkbox => {
            const badge = checkbox.closest('.roles-badge');
            const avatarElement = badge.querySelector('.integrante-avatar, .integrante-avatar-placeholder');
            const nombreElement = badge.querySelector('.integrante-nombre');
            const emailElement = badge.querySelector('.integrante-email');

            // Clonar el badge pero sin el checkbox
            const selectedBadge = document.createElement('div');
            selectedBadge.className = 'roles-badge selected-integrante';
            selectedBadge.innerHTML = `
                ${avatarElement.outerHTML}
                <div class="integrante-info">
                    <div class="integrante-nombre">${nombreElement.textContent}</div>
                    <div class="integrante-email">${emailElement.textContent}</div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger remove-integrante" data-user-id="${checkbox.value}" title="Remover integrante">
                    <i class="bi bi-x"></i>
                </button>
            `;

            seleccionadosContainer.appendChild(selectedBadge);
        });

        // Agregar event listeners para remover integrantes
        document.querySelectorAll('.remove-integrante').forEach(btn => {
            btn.addEventListener('click', function() {
                const userId = this.getAttribute('data-user-id');
                const checkbox = document.querySelector(`.roles-badge input[type="checkbox"][value="${userId}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                    const badge = checkbox.closest('.roles-badge');
                    setBadgeState(badge, false);
                    updateIntegrantesField();
                }
            });
        });
    };

    // Configuración inicial de badges interactivos
    document.querySelectorAll('.roles-badge').forEach(badge => {
        const checkbox = badge.querySelector('input[type="checkbox"]');
        badge.setAttribute('role', 'checkbox');
        badge.setAttribute('tabindex', '0');

        // Aplicar estado inicial
        setBadgeState(badge, checkbox.checked);

        badge.addEventListener('click', function(event) {
            event.preventDefault();
            checkbox.checked = !checkbox.checked;
            setBadgeState(badge, checkbox.checked);
            updateIntegrantesField();
        });

        badge.addEventListener('keydown', function(event) {
            if (event.key === ' ' || event.key === 'Enter') {
                event.preventDefault();
                checkbox.checked = !checkbox.checked;
                setBadgeState(badge, checkbox.checked);
                updateIntegrantesField();
            }
        });
    });

    // Toggle de estado activo/inactivo
    const activeToggle = document.querySelector('.active-status-toggle');
    if (activeToggle) {
        const checkbox = activeToggle.querySelector('input[type="checkbox"]');
        const textElement = activeToggle.querySelector('.active-status-text');

        const updateActiveState = (isChecked) => {
            textElement.textContent = isChecked ? 'Sí, activo' : 'No, inactivo';
        };

        updateActiveState(checkbox.checked);

        activeToggle.addEventListener('click', function(event) {
            if (event.target === checkbox) return;
            event.preventDefault();
            checkbox.checked = !checkbox.checked;
            updateActiveState(checkbox.checked);
        });

        activeToggle.addEventListener('keydown', function(event) {
            if (event.key === ' ' || event.key === 'Enter') {
                event.preventDefault();
                checkbox.checked = !checkbox.checked;
                updateActiveState(checkbox.checked);
            }
        });
    }

    // 🔍 Búsqueda en tiempo real (filtrado por inicio de nombre o email)
    const searchInput = document.getElementById('integrantesSearchInput');
    const usuariosContainer = document.getElementById('usuarios-disponibles');

    const filterUsers = (searchTerm) => {
        const badges = usuariosContainer.querySelectorAll('.roles-badge');
        let visibleCount = 0;
        const searchLower = searchTerm.toLowerCase();

        badges.forEach(badge => {
            const nombreElement = badge.querySelector('.integrante-nombre');
            const emailElement = badge.querySelector('.integrante-email');

            if (nombreElement && emailElement) {
                const nombre = nombreElement.textContent.toLowerCase();
                const email = emailElement.textContent.toLowerCase();

                // ✅ Filtrar SOLO si comienza con el término de búsqueda
                const isVisible = 
                    nombre.startsWith(searchLower) || 
                    email.startsWith(searchLower);

                badge.style.display = isVisible ? '' : 'none';
                if (isVisible) {
                    visibleCount++;
                }
            }
        });

        // Mostrar/ocultar mensaje de "no resultados"
        let noResultsMsg = usuariosContainer.querySelector('.no-results-message');
        if (visibleCount === 0 && searchTerm.trim() !== '') {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.className = 'no-results-message alert alert-info mt-3';
                noResultsMsg.innerHTML = '<i class="bi bi-info-circle"></i> No se encontraron usuarios que coincidan con la búsqueda.';
                usuariosContainer.appendChild(noResultsMsg);
            }
            noResultsMsg.style.display = 'block';
        } else if (noResultsMsg) {
            noResultsMsg.style.display = 'none';
        }
    };

    // Event listeners para la búsqueda
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.trim();
            filterUsers(searchTerm);
        });

        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                this.value = '';
                filterUsers('');
                this.blur();
            }
        });
    }

    // Inicializar estado del formulario
    updateIntegrantesField();
});