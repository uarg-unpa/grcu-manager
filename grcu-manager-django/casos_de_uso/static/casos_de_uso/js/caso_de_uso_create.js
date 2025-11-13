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
    
    // ===== Control de límite de caracteres en Observaciones =====
    const observacionesTextarea = document.querySelector('textarea[name="observaciones"]');
    const observacionesContador = document.getElementById('observaciones-contador');
    const maxCaracteresObservaciones = 5000;
    
    if (observacionesTextarea && observacionesContador) {
        // Función para actualizar el contador
        function actualizarContadorObservaciones() {
            const longitudActual = observacionesTextarea.value.length;
            observacionesContador.textContent = `${longitudActual} / ${maxCaracteresObservaciones}`;
            
            // Cambiar color según el progreso
            if (longitudActual >= maxCaracteresObservaciones) {
                observacionesContador.classList.remove('bg-secondary', 'bg-warning');
                observacionesContador.classList.add('bg-danger');
            } else if (longitudActual >= maxCaracteresObservaciones * 0.9) {
                observacionesContador.classList.remove('bg-secondary', 'bg-danger');
                observacionesContador.classList.add('bg-warning');
            } else {
                observacionesContador.classList.remove('bg-warning', 'bg-danger');
                observacionesContador.classList.add('bg-secondary');
            }
        }
        
        // Función para prevenir exceder el límite al escribir
        function controlarLimiteObservaciones(e) {
            const longitudActual = observacionesTextarea.value.length;
            const teclasPermitidas = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'Tab'];
            
            if (longitudActual >= maxCaracteresObservaciones && !teclasPermitidas.includes(e.key) && !e.ctrlKey && !e.metaKey) {
                e.preventDefault();
                return false;
            }
        }
        
        // Función para truncar si se pega texto que excede el límite
        function controlarPegadoObservaciones(e) {
            setTimeout(() => {
                if (observacionesTextarea.value.length > maxCaracteresObservaciones) {
                    observacionesTextarea.value = observacionesTextarea.value.substring(0, maxCaracteresObservaciones);
                    actualizarContadorObservaciones();
                }
            }, 10);
        }
        
        // Agregar event listeners
        observacionesTextarea.addEventListener('input', actualizarContadorObservaciones);
        observacionesTextarea.addEventListener('keydown', controlarLimiteObservaciones);
        observacionesTextarea.addEventListener('paste', controlarPegadoObservaciones);
        
        // Actualizar contador al cargar
        actualizarContadorObservaciones();
    }
});
