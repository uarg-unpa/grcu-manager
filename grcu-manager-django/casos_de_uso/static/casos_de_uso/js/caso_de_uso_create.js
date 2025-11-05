document.addEventListener('DOMContentLoaded', function() {
    // ===== Control de límite de caracteres en Descripción =====
    const descripcionTextarea = document.querySelector('textarea[name="descripcion"]');
    const descripcionContador = document.getElementById('descripcion-contador');
    const maxCaracteres = 2500;
    
    if (descripcionTextarea && descripcionContador) {
        // Función para actualizar el contador
        function actualizarContador() {
            const longitudActual = descripcionTextarea.value.length;
            descripcionContador.textContent = `${longitudActual} / ${maxCaracteres}`;
            // Cambiar color según el progreso
            if (longitudActual >= maxCaracteres) {
                descripcionContador.classList.remove('bg-secondary', 'bg-warning');
                descripcionContador.classList.add('bg-danger');
            } else if (longitudActual >= maxCaracteres * 0.9) {
                descripcionContador.classList.remove('bg-secondary', 'bg-danger');
                descripcionContador.classList.add('bg-warning');
            } else {
                descripcionContador.classList.remove('bg-warning', 'bg-danger');
                descripcionContador.classList.add('bg-secondary');
            }
        }
        // Función para prevenir exceso de caracteres
        function controlarLimite(e) {
            const longitudActual = descripcionTextarea.value.length;
            // Permitir teclas especiales (backspace, delete, arrows, etc.)
            const teclasPermitidas = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Tab'];
            if (longitudActual >= maxCaracteres && !teclasPermitidas.includes(e.key) && !e.ctrlKey && !e.metaKey) {
                e.preventDefault();
                return false;
            }
        }
        // Función para truncar si se pega texto que excede el límite
        function controlarPegado(e) {
            setTimeout(() => {
                if (descripcionTextarea.value.length > maxCaracteres) {
                    descripcionTextarea.value = descripcionTextarea.value.substring(0, maxCaracteres);
                    actualizarContador();
                }
            }, 10);
        }
        // Agregar event listeners
        descripcionTextarea.addEventListener('input', actualizarContador);
        descripcionTextarea.addEventListener('keydown', controlarLimite);
        descripcionTextarea.addEventListener('paste', controlarPegado);
        // Actualizar contador al cargar
        actualizarContador();
    }
});
