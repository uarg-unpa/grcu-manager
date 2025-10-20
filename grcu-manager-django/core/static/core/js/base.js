/**
 * CORE - Base Template JavaScript
 * Funcionalidad común para todas las páginas del sistema
 */

/**
 * Manejo del scroll del header
 * Reduce el tamaño del header cuando se hace scroll
 */
document.addEventListener('scroll', function() {
    const header = document.querySelector('.custom-header');
    if (!header) return;
    
    if (window.scrollY > 60) {
        header.classList.add('shrink');
    } else {
        header.classList.remove('shrink');
    }
});

/**
 * Inicialización cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar tooltips de Bootstrap
    initializeTooltips();
    
    // Auto-ocultar mensajes de alerta
    autoHideAlerts();
});

/**
 * Inicializa todos los tooltips de Bootstrap en la página
 * Busca elementos con data-bs-toggle="tooltip" y los activa
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-oculta los mensajes de alerta después de 5 segundos
 * Aplica a todos los elementos con clase .alert
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5 segundos
    });
}
