// proyectos/static/proyectos/js/gestionar_integrantes.js
// JS para confirmación de cambios en la gestión de roles de integrantes

document.addEventListener('DOMContentLoaded', function() {
    // Confirmar antes de enviar el formulario
    const form = document.getElementById('formGestionIntegrantes');
    if (form) {
        form.addEventListener('submit', function(e) {
            const cambios = Array.from(form.querySelectorAll('select[name^="rol_"]'))
                .filter(select => !select.disabled)
                .length;
            if (cambios > 0) {
                const confirmar = confirm('¿Estás seguro de que deseas actualizar los roles de los integrantes?');
                if (!confirmar) {
                    e.preventDefault();
                }
            }
        });
    }
});
