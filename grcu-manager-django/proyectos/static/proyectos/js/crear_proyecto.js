document.addEventListener('DOMContentLoaded', function() {
    const grupoSelect = document.getElementById('id_grupo');
    const liderSelect = document.getElementById('id_lider');

    // Función para cargar integrantes del grupo seleccionado
    function cargarIntegrantes(grupoId) {
        if (!grupoId) {
            liderSelect.innerHTML = '<option value="">Selecciona primero un grupo</option>';
            liderSelect.disabled = true;
            return;
        }
        liderSelect.disabled = false;
        liderSelect.innerHTML = '<option value="">Cargando...</option>';
        const url = `/grupos/api/grupo/${grupoId}/integrantes/`;
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                liderSelect.innerHTML = '<option value="">Selecciona un líder</option>';
                if (data.integrantes && data.integrantes.length > 0) {
                    data.integrantes.forEach(integrante => {
                        const option = document.createElement('option');
                        option.value = integrante.id;
                        option.textContent = `${integrante.nombre} (${integrante.email})`;
                        liderSelect.appendChild(option);
                    });
                } else {
                    liderSelect.innerHTML = '<option value="">No hay integrantes en este grupo</option>';
                }
            })
            .catch(error => {
                liderSelect.innerHTML = '<option value="">Error al cargar integrantes</option>';
            });
    }

    grupoSelect.addEventListener('change', function() {
        const grupoId = this.value;
        cargarIntegrantes(grupoId);
    });

    if (grupoSelect.value) {
        cargarIntegrantes(grupoSelect.value);
    }
});
