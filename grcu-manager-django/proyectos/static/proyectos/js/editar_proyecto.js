// Función para cargar integrantes del grupo seleccionado
function cargarIntegrantes(grupoId) {
    const liderSelect = document.getElementById('id_lider');
    const currentLiderId = liderSelect.dataset.currentLider;
    
    console.log('cargarIntegrantes llamado con grupoId:', grupoId);
    console.log('Líder actual:', currentLiderId);
    
    if (!grupoId) {
        liderSelect.innerHTML = '<option value="">Selecciona primero un grupo</option>';
        liderSelect.disabled = true;
        return;
    }

    // Habilitar el select de líder
    liderSelect.disabled = false;

    // Mostrar loading
    liderSelect.innerHTML = '<option value="">Cargando...</option>';

    const url = `/grupos/api/grupo/${grupoId}/integrantes/`;
    console.log('Haciendo fetch a:', url);

    // Hacer petición AJAX para obtener los integrantes
    fetch(url)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            liderSelect.innerHTML = '<option value="">Selecciona un líder</option>';
            
            if (data.integrantes && data.integrantes.length > 0) {
                data.integrantes.forEach(integrante => {
                    const option = document.createElement('option');
                    option.value = integrante.id;
                    option.textContent = `${integrante.nombre} (${integrante.email})`;
                    
                    // Preseleccionar el líder actual
                    if (currentLiderId && integrante.id == currentLiderId) {
                        option.selected = true;
                    }
                    
                    liderSelect.appendChild(option);
                });
            } else {
                liderSelect.innerHTML = '<option value="">No hay integrantes en este grupo</option>';
            }
        })
        .catch(error => {
            console.error('Error al cargar integrantes:', error);
            liderSelect.innerHTML = '<option value="">Error al cargar integrantes</option>';
        });
}

// Cargar integrantes del grupo actual al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const grupoSelect = document.getElementById('id_grupo');
    const liderSelect = document.getElementById('id_lider');
    
    console.log('Script editar_proyecto.js cargado');
    console.log('Grupo select:', grupoSelect);
    console.log('Lider select:', liderSelect);
    
    // Event listener para cambio de grupo
    if (grupoSelect) {
        grupoSelect.addEventListener('change', function() {
            const grupoId = this.value;
            console.log('Grupo cambiado a:', grupoId);
            cargarIntegrantes(grupoId);
        });
        
        // Cargar integrantes del grupo preseleccionado
        if (grupoSelect.value) {
            console.log('Cargando integrantes del grupo:', grupoSelect.value);
            cargarIntegrantes(grupoSelect.value);
        }
    }
});

// Safety: asegurar que el botón de guardar dispare el submit incluso si
// algún otro script intercepta/previen el evento. Esto fuerza el envío
// y además deja un log útil para depuración.
document.addEventListener('DOMContentLoaded', function() {
    try {
        const form = document.getElementById('proyectoForm');
        const guardarBtn = document.querySelector('.proyecto-form-btn-crear');
        if (form && guardarBtn) {
            guardarBtn.addEventListener('click', function(e) {
                console.log('Forzando submit desde editar_proyecto.js');
                // Ejecutar submit explícitamente en el siguiente tick
                setTimeout(function() {
                    try {
                        form.submit();
                    } catch (err) {
                        console.error('Error al forzar submit:', err);
                    }
                }, 0);
            });
        }
    } catch (err) {
        console.error('Error al inicializar forzado de submit:', err);
    }
});
