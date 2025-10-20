/**
 * lider_dashboard.js
 * 
 * Funcionalidad de gráficos y tooltips para el Dashboard del Líder.
 * Incluye gráficos de tipo doughnut (Chart.js) para mostrar distribución
 * de requerimientos y casos de uso (huérfanos vs relacionados).
 */

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar tooltips de Bootstrap
    initializeDashboardTooltips();
    
    // Obtener datos de los proyectos desde el data attribute
    const dashboardDataElement = document.getElementById('dashboard-data');
    if (!dashboardDataElement) {
        console.warn('No se encontraron datos del dashboard');
        return;
    }
    
    let dashboardData;
    try {
        dashboardData = JSON.parse(dashboardDataElement.textContent);
    } catch (error) {
        console.error('Error al parsear datos del dashboard:', error);
        return;
    }
    
    // Renderizar gráficos para cada proyecto
    dashboardData.forEach((proyecto, index) => {
        renderGraficoRequerimientos(proyecto, index);
        renderGraficoCasosUso(proyecto, index);
    });
});

/**
 * Inicializa los tooltips de Bootstrap para el dashboard.
 * 
 * @function initializeDashboardTooltips
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
 * Renderiza el gráfico de distribución de requerimientos.
 * Muestra la proporción de requerimientos huérfanos vs relacionados.
 * 
 * @param {Object} proyecto - Datos del proyecto
 * @param {number} index - Índice del proyecto en el dashboard
 */
function renderGraficoRequerimientos(proyecto, index) {
    const canvasId = `grafico-req-${index}`;
    const ctx = document.getElementById(canvasId);
    
    if (!ctx) {
        console.warn(`Canvas ${canvasId} no encontrado`);
        return;
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Huérfanos', 'Relacionados'],
            datasets: [{
                data: [
                    proyecto.reqs_huerfanos_count,
                    proyecto.reqs_relacionados_count
                ],
                backgroundColor: [
                    '#EF4444',  // Rojo para huérfanos
                    '#3B82F6'   // Azul para relacionados
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: { 
                    display: true, 
                    position: 'bottom' 
                }
            },
            cutout: '65%'
        }
    });
}

/**
 * Renderiza el gráfico de distribución de casos de uso.
 * Muestra la proporción de casos de uso huérfanos vs relacionados.
 * 
 * @param {Object} proyecto - Datos del proyecto
 * @param {number} index - Índice del proyecto en el dashboard
 */
function renderGraficoCasosUso(proyecto, index) {
    const canvasId = `grafico-cu-${index}`;
    const ctx = document.getElementById(canvasId);
    
    if (!ctx) {
        console.warn(`Canvas ${canvasId} no encontrado`);
        return;
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Huérfanos', 'Relacionados'],
            datasets: [{
                data: [
                    proyecto.casos_huerfanos_count,
                    proyecto.casos_relacionados_count
                ],
                backgroundColor: [
                    '#EF4444',  // Rojo para huérfanos
                    '#10B981'   // Verde para relacionados
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: { 
                    display: true, 
                    position: 'bottom' 
                }
            },
            cutout: '65%'
        }
    });
}
