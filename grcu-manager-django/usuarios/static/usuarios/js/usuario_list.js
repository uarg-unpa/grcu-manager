document.addEventListener('DOMContentLoaded', function(){
    // 🔍 Búsqueda en tiempo real (filtrado por inicio de nombre o email)
    const searchInput = document.getElementById('usuariosSearchInput');
    const usuariosTableBody = document.getElementById('usuariosTableBody');

    const filterUsers = (searchTerm) => {
        const rows = usuariosTableBody.querySelectorAll('tr[data-user-id]');
        let visibleCount = 0;
        const searchLower = searchTerm.toLowerCase();

        rows.forEach(row => {
            const nombreElement = row.querySelector('td:nth-child(4)'); // Columna de nombre
            const emailElement = row.querySelector('td:nth-child(5)'); // Columna de email

            if (nombreElement && emailElement) {
                const nombre = nombreElement.textContent.toLowerCase();
                const email = emailElement.textContent.toLowerCase();

                // ✅ Filtrar SOLO si comienza con el término de búsqueda
                const isVisible =
                    nombre.startsWith(searchLower) ||
                    email.startsWith(searchLower);

                row.style.display = isVisible ? '' : 'none';
                if (isVisible) {
                    visibleCount++;
                }
            }
        });

        // Mostrar/ocultar mensaje de "no resultados"
        let noResultsMsg = usuariosTableBody.querySelector('.no-results-message');
        if (visibleCount === 0 && searchTerm.trim() !== '') {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('tr');
                noResultsMsg.className = 'no-results-message';
                noResultsMsg.innerHTML = '<td colspan="7" class="text-center alert alert-info"><i class="bi bi-info-circle"></i> No se encontraron usuarios que coincidan con la búsqueda.</td>';
                usuariosTableBody.appendChild(noResultsMsg);
            }
            noResultsMsg.style.display = '';
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

    // Funcionalidad de selección múltiple
    const selectAll = document.getElementById('selectAllUsers');
    const checkboxes = Array.from(document.querySelectorAll('.row-checkbox'));
    if(selectAll){
        selectAll.addEventListener('change', function(){
            checkboxes.forEach(cb => {
                cb.checked = selectAll.checked;
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
});