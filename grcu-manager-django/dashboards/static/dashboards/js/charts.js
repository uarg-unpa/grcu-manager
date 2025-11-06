// Gráficos del dashboard - versión simplificada
document.addEventListener('DOMContentLoaded', function() {
    // Esperar un poco para asegurar que todo esté cargado
    setTimeout(function() {
        initializeCharts();
    }, 100);
});

function initializeCharts() {
    // Procesar todos los canvas que tengan atributos data-labels y data-values
    const canvases = document.querySelectorAll('canvas[data-labels][data-values]');

    canvases.forEach(function(canvas) {
        // Verificar si ya se creó un chart para este canvas
        if (canvas.dataset.chartCreated === 'true') {
            return;
        }

        const labelsRaw = canvas.dataset.labels || '[]';
        const valuesRaw = canvas.dataset.values || '[]';

        let labels, values;
        try {
            labels = JSON.parse(labelsRaw);
            values = JSON.parse(valuesRaw);
        } catch (e) {
            return; // Silenciar errores para evitar loops
        }

        const type = canvas.dataset.type || 'doughnut';
        const colorsRaw = canvas.dataset.colors || null;
        let colors = [];
        if (colorsRaw) {
            try { colors = JSON.parse(colorsRaw); } catch(e) { colors = null; }
        }
        if (!colors || colors.length !== labels.length) {
            colors = ['#007bff', '#28a745', '#ffc107', '#6c757d', '#17a2b8', '#20c997'];
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) {
            return;
        }

        // Configuración con leyendas completas
        const config = {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 6,
                            font: {
                                size: 10
                            },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const meta = chart.getDatasetMeta(0);
                                        const style = meta.controller.getStyle(i);
                                        return {
                                            text: label,
                                            fillStyle: style.backgroundColor,
                                            strokeStyle: style.borderColor,
                                            lineWidth: style.borderWidth,
                                            hidden: false,
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            }
        };

        try {
            new Chart(ctx, config);
            canvas.dataset.chartCreated = 'true';
        } catch (e) {
            // Silenciar errores
        }
    });
}
