// proyectos/static/proyectos/js/proyecto_reportes.js
// JS para inicialización de gráficos en la vista de reportes de proyecto

document.addEventListener('DOMContentLoaded', function() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false
            }
        }
    };

    // Gráfico de Tipo
    new Chart(document.getElementById('tipoChart'), {
        type: 'doughnut',
        data: window.tipoChartData,
        options: chartOptions
    });

    // Gráfico de Estado
    new Chart(document.getElementById('estadoChart'), {
        type: 'bar',
        data: window.estadoChartData,
        options: {
            ...chartOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });

    // Gráfico de Trazabilidad Requerimientos
    new Chart(document.getElementById('trazabilidadReqsChart'), {
        type: 'doughnut',
        data: window.trazabilidadReqsChartData,
        options: chartOptions
    });

    // Gráfico de Trazabilidad Casos
    new Chart(document.getElementById('trazabilidadCasosChart'), {
        type: 'doughnut',
        data: window.trazabilidadCasosChartData,
        options: chartOptions
    });
});
