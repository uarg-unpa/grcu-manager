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

        // Configuración simple sin opciones problemáticas
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
                responsive: false,  // Desactivar responsive para evitar loops
                plugins: {
                    legend: {
                        display: false  // Ocultar leyenda para ahorrar espacio
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
