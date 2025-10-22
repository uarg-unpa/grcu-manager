/**
 * Dashboard de Auditoría - JavaScript
 * Maneja la inicialización y configuración de gráficos Chart.js
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráficos cuando el DOM esté listo
    initializeCharts();

    // Configurar filtros dinámicos si es necesario
    setupFilters();
});

/**
 * Inicializa todos los gráficos del dashboard
 */
function initializeCharts() {
    // Gráfico de actividades por día
    initializeActividadesPorDiaChart();
}

/**
 * Inicializa el gráfico de actividades por día
 */
function initializeActividadesPorDiaChart() {
    const ctx = document.getElementById('actividadesPorDiaChart');

    if (!ctx) {
        console.warn('Canvas para gráfico de actividades por día no encontrado');
        return;
    }

    // Datos del gráfico (pasados desde el template Django)
    const chartData = window.auditoriaChartData || {
        labels: [],
        data: []
    };

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Actividades',
                data: chartData.data,
                borderColor: 'rgb(13, 110, 253)',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgb(13, 110, 253)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: 'rgb(13, 110, 253)',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(13, 110, 253)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            return 'Fecha: ' + context[0].label;
                        },
                        label: function(context) {
                            return 'Actividades: ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 11
                        }
                    },
                    title: {
                        display: true,
                        text: 'Número de Actividades',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    },
                    title: {
                        display: true,
                        text: 'Fecha',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });

    // Agregar funcionalidad de zoom si no hay datos
    if (chartData.data.length === 0) {
        addNoDataMessage(ctx);
    }
}

/**
 * Agrega un mensaje cuando no hay datos para mostrar
 */
function addNoDataMessage(canvas) {
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#6c757d';
    ctx.font = '16px Arial';
    ctx.fillText('No hay datos disponibles para el período seleccionado', centerX, centerY);
    ctx.restore();
}

/**
 * Configura los filtros dinámicos
 */
function setupFilters() {
    // Auto-submit del formulario cuando cambian los filtros principales
    const filterElements = ['#accion', '#usuario'];

    filterElements.forEach(selector => {
        const element = document.querySelector(selector);
        if (element) {
            element.addEventListener('change', function() {
                // Pequeño delay para evitar submits excesivos
                clearTimeout(window.filterTimeout);
                window.filterTimeout = setTimeout(() => {
                    element.closest('form').submit();
                }, 300);
            });
        }
    });

    // Mejorar la experiencia de los datepickers
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Validar que fecha_desde <= fecha_hasta
            const fechaDesde = document.getElementById('fecha_desde');
            const fechaHasta = document.getElementById('fecha_hasta');

            if (fechaDesde && fechaHasta && fechaDesde.value && fechaHasta.value) {
                if (new Date(fechaDesde.value) > new Date(fechaHasta.value)) {
                    alert('La fecha "Desde" no puede ser posterior a la fecha "Hasta"');
                    this.value = '';
                    return;
                }
            }
        });
    });

    // Funcionalidad de búsqueda en tiempo real (opcional)
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Aquí se podría implementar búsqueda AJAX
                // Por ahora, solo se busca al presionar Enter
            }, 500);
        });
    }
}

/**
 * Función de utilidad para mostrar mensajes de carga
 */
function showLoadingMessage(element, message = 'Cargando...') {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }

    if (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center align-items-center p-4">
                <div class="spinner-border text-primary me-2" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <span>${message}</span>
            </div>
        `;
    }
}

/**
 * Función de utilidad para ocultar mensajes de carga
 */
function hideLoadingMessage(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }

    if (element && element.querySelector('.spinner-border')) {
        element.innerHTML = '';
    }
}

// Exponer funciones globales para uso desde templates
window.AuditoriaDashboard = {
    initializeCharts: initializeCharts,
    setupFilters: setupFilters,
    showLoadingMessage: showLoadingMessage,
    hideLoadingMessage: hideLoadingMessage
};