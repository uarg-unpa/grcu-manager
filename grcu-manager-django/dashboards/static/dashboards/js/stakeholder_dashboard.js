// dashboards/static/dashboards/js/stakeholder_dashboard.js
// JS para el dashboard de stakeholders

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips si existen
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('Stakeholder dashboard loaded');
});
