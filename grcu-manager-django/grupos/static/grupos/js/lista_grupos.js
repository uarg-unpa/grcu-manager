document.addEventListener('DOMContentLoaded', function(){
    const searchInput = document.getElementById('gruposSearchInput');
    const gruposTableBody = document.getElementById('gruposTableBody');
    let searchTimeout;
    let isSearching = false;

    const renderRow = (g) => {
        const logoHtml = g.logo ? `<img src="${g.logo}" width="50" height="50" style="object-fit:cover; border-radius:6px;">` : `<span class="grupo-lista-texto-muted">Sin logo</span>`;
        const integrantesHtml = g.integrantes && g.integrantes.length ? g.integrantes.join(', ') : '<span class="grupo-lista-texto-muted">Sin integrantes</span>';
        const activoHtml = g.activo ? '<i class="bi bi-check-circle-fill text-success"></i>' : '<i class="bi bi-x-circle-fill text-danger"></i>';

        return `
            <tr>
                <td class="text-start">${logoHtml}</td>
                <td class="text-start">${g.nombre}</td>
                <td class="text-start">${integrantesHtml}</td>
                <td class="text-start">${activoHtml}</td>
                <td class="text-center">
                    <a href="/grupos/editar/${g.id}/" class="btn btn-sm btn-outline-warning grupo-btn-edit" title="Editar grupo" data-bs-toggle="tooltip"><i class="bi bi-pencil-square"></i></a>
                    <a href="/grupos/eliminar/${g.id}/" class="btn btn-sm btn-outline-danger grupo-btn-delete" title="Eliminar grupo" data-bs-toggle="tooltip"><i class="bi bi-trash"></i></a>
                </td>
            </tr>
        `;
    };

    const searchGrupos = async (term) => {
        if (term.trim() === '') {
            window.location.href = window.location.pathname;
            return;
        }

        isSearching = true;
        try {
            const resp = await fetch(`/grupos/buscar/?q=${encodeURIComponent(term)}`);
            const data = await resp.json();

            gruposTableBody.innerHTML = '';
            if (data.count === 0) {
                gruposTableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center alert alert-info"><i class="bi bi-info-circle"></i> No se encontraron grupos que coincidan con "${term}".</td>
                    </tr>
                `;
            } else {
                data.grupos.forEach(g => {
                    gruposTableBody.insertAdjacentHTML('beforeend', renderRow(g));
                });
            }
        } catch (err) {
            console.error('Error búsqueda grupos:', err);
            gruposTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center alert alert-danger"><i class="bi bi-exclamation-triangle"></i> Error al buscar grupos. Intenta nuevamente.</td>
                </tr>
            `;
        } finally {
            isSearching = false;
        }
    };

    if (searchInput) {
        searchInput.addEventListener('input', function(){
            const term = this.value.trim();
            clearTimeout(searchTimeout);
            if (isSearching) return;
            searchTimeout = setTimeout(() => {
                searchGrupos(term);
            }, 300);
        });

        searchInput.addEventListener('keydown', function(e){
            if (e.key === 'Escape') {
                this.value = '';
                clearTimeout(searchTimeout);
                window.location.href = window.location.pathname;
            }
            if (e.key === 'Enter') {
                e.preventDefault();
                clearTimeout(searchTimeout);
                searchGrupos(this.value.trim());
            }
        });

        const gruposSearchBtn = document.querySelector('.grupo-lista-search .input-group-text');
        if (gruposSearchBtn) {
            gruposSearchBtn.addEventListener('click', function() {
                clearTimeout(searchTimeout);
                searchGrupos(searchInput.value.trim());
            });
        }
    }
});
