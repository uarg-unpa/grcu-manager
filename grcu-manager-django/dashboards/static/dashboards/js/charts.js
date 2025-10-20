document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que Chart.js esté disponible
    if (typeof Chart === 'undefined') {
        console.error('Chart.js no está disponible');
        return;
    }

    // Helper para crear colores aleatorios consistentes
    function randomColor(alpha=0.8){
        const r = Math.floor(Math.random()*200)+30;
        const g = Math.floor(Math.random()*200)+30;
        const b = Math.floor(Math.random()*200)+30;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    // Procesar todos los canvas que tengan atributos data-labels y data-values
    document.querySelectorAll('canvas[data-labels][data-values]').forEach(canvas => {
        // Verificar si ya se creó un chart para este canvas
        if (canvas.dataset.chartCreated === 'true') {
            console.log('Chart ya creado para', canvas.id);
            return;
        }

        const labelsRaw = canvas.dataset.labels || '[]';
        const valuesRaw = canvas.dataset.values || '[]';
        let labels, values;
        try {
            labels = JSON.parse(labelsRaw);
            values = JSON.parse(valuesRaw);
        } catch (e) {
            console.error('Error parseando datos para chart en', canvas.id, e);
            return;
        }

        const type = canvas.dataset.type || 'doughnut';
        const colorsRaw = canvas.dataset.colors || null;
        let colors = [];
        if (colorsRaw) {
            try { colors = JSON.parse(colorsRaw); } catch(e) { colors = null; }
        }
        if (!colors || colors.length !== labels.length) {
            colors = labels.map(()=>randomColor(0.75));
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const config = {
            type: type,
            data: {
                labels: labels,
                datasets: [{ data: values, backgroundColor: colors }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        };

        // Customize some chart types
        if (type === 'bar' && canvas.dataset.horizontal === 'true') {
            config.options.indexAxis = 'y';
            config.options.scales = { x: { beginAtZero: true } };
        } else if (type === 'bar') {
            config.options.scales = { y: { beginAtZero: true } };
        }

        // Try to create chart
        try {
            new Chart(ctx, config);
            // Marcar el canvas como procesado
            canvas.dataset.chartCreated = 'true';
        } catch (e) {
            console.error('Chart.js error for', canvas.id, e);
        }
    });
});
