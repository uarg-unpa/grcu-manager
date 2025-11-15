document.addEventListener('DOMContentLoaded', function(){
    const searchInput = document.getElementById('proyectosSearchInput');
    const proyectosTableBody = document.getElementById('proyectosTableBody');
    let searchTimeout;
    let isSearching = false;

    const renderRow = (p) => {
        const logoHtml = p.logo ? `<img src="${p.logo}" width="150" height="150" style="object-fit:contain; border-radius:12px; box-shadow:0 2px 8px rgba(68,76,138,0.10); border:2px solid #eee; background:#fff; padding:8px;">` : `<span class="text-muted">Sin logo</span>`;
        const clientesHtml = p.clientes && p.clientes.length ? `<ul class="list-unstyled mb-0">${p.clientes.map(c => `<li><i class="bi bi-person-badge text-info"></i> ${c}</li>`).join('')}</ul>` : `<span class="text-muted">Sin clientes</span>`;

        return `
            <tr>
                <td class="text-start">${logoHtml}</td>
                <td class="text-start">${p.nombre}</td>
                <td class="text-start">${p.lider ? p.lider : '<span class="text-muted">No asignado</span>'}</td>
                <td class="text-start">${clientesHtml}</td>
                <td class="text-start">${p.creado_por ? p.creado_por : '<span class="text-muted">Desconocido</span>'}</td>
                <td class="text-start">${p.fecha_creacion}</td>
                <td class="text-center">
                    <a href="/proyectos/${p.id}/detail/" class="btn btn-sm btn-outline-primary proyecto-btn-view" title="Ver detalles" data-bs-toggle="tooltip"><i class="bi bi-eye-fill"></i></a>
                    <a href="/proyectos/editar/${p.id}/" class="btn btn-sm btn-outline-warning proyecto-btn-edit" title="Editar proyecto" data-bs-toggle="tooltip"><i class="bi bi-pencil-square"></i></a>
                    <a href="/proyectos/eliminar/${p.id}/" class="btn btn-sm btn-outline-danger proyecto-btn-delete" title="Eliminar proyecto" data-bs-toggle="tooltip"><i class="bi bi-trash"></i></a>
                </td>
            </tr>
        `;
    };

    const searchProyectos = async (term) => {
        if (term.trim() === '') {
            // Vacío: recargar la página para mostrar todos
            window.location.href = window.location.pathname;
            return;
        }

        isSearching = true;
        try {
            const resp = await fetch(`/proyectos/buscar/?q=${encodeURIComponent(term)}`);
            const data = await resp.json();

            proyectosTableBody.innerHTML = '';
            if (data.count === 0) {
                proyectosTableBody.innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center alert alert-info"><i class="bi bi-info-circle"></i> No se encontraron proyectos que coincidan con "${term}".</td>
                    </tr>
                `;
            } else {
                data.proyectos.forEach(p => {
                    proyectosTableBody.insertAdjacentHTML('beforeend', renderRow(p));
                });
            }
        } catch (err) {
            console.error('Error búsqueda proyectos:', err);
            proyectosTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center alert alert-danger"><i class="bi bi-exclamation-triangle"></i> Error al buscar proyectos. Intenta nuevamente.</td>
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
                searchProyectos(term);
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
                searchProyectos(this.value.trim());
            }
        });

        // Click en el icono de búsqueda
        const proyectosSearchBtn = document.querySelector('.proyecto-lista-search .input-group-text');
        if (proyectosSearchBtn) {
            proyectosSearchBtn.addEventListener('click', function() {
                clearTimeout(searchTimeout);
                searchProyectos(searchInput.value.trim());
            });
        }
    }
});
