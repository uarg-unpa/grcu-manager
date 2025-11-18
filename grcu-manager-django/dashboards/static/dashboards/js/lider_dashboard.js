/**
 * lider_dashboard.js v9.0
 * 
 * Funcionalidad adicional para el Dashboard del Líder.
 * Los gráficos se manejan automáticamente en charts.js
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log('Dashboard del Líder inicializado v9.0');
    
    // Inicializar tooltips de Bootstrap
    initializeDashboardTooltips();
    
    // Animar números en las tarjetas
    setTimeout(() => {
        animateNumbers();
    }, 200);
});

/**
 * Inicializa los tooltips de Bootstrap para el dashboard.
 */
function initializeDashboardTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Anima los números de las tarjetas principales
 */
function animateNumbers() {
    const numbers = document.querySelectorAll('.metric-value');
    
    numbers.forEach((numberEl, index) => {
        const text = numberEl.textContent.trim();
        const finalValue = parseInt(text) || 0;
        if (finalValue === 0) return;
        
        let currentValue = 0;
        const duration = 1000;
        const increment = finalValue / (duration / 16);
        
        const animate = () => {
            currentValue += increment;
            if (currentValue < finalValue) {
                numberEl.textContent = Math.floor(currentValue);
                requestAnimationFrame(animate);
            } else {
                numberEl.textContent = finalValue;
            }
        };
        
        setTimeout(() => animate(), index * 50);
    });
}
