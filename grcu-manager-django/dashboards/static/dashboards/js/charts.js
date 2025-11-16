/**
 * charts.js v9.0
 * 
 * Renderiza gráficos automáticamente usando data-attributes
 */

function initializeCharts() {
    console.log('Inicializando gráficos...');
    const canvases = document.querySelectorAll('canvas[data-labels][data-values]');
    console.log(`Se encontraron ${canvases.length} canvas con data-attributes`);
    
    canvases.forEach((canvas, index) => {
        try {
            // Prevenir inicialización múltiple
            if (canvas.dataset.chartCreated === 'true') {
                console.log(`Canvas ${canvas.id} ya fue inicializado, omitiendo`);
                return;
            }
            
            console.log(`Procesando canvas #${index + 1}: ${canvas.id}`);
            
            const labels = JSON.parse(canvas.dataset.labels);
            const values = JSON.parse(canvas.dataset.values);
            const type = canvas.dataset.type || 'doughnut';
            const colors = canvas.dataset.colors ? JSON.parse(canvas.dataset.colors) : null;
            
            console.log(`  - Type: ${type}`);
            console.log(`  - Labels:`, labels);
            console.log(`  - Values:`, values);
            console.log(`  - Colors:`, colors);
            
            const ctx = canvas.getContext('2d');
            
            const config = {
                type: type,
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: colors || [
                            '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                            '#ec4899', '#14b8a6', '#f97316', '#6366f1'
                        ],
                        borderColor: '#ffffff',
                        borderWidth: type === 'bar' ? 0 : 3,
                        hoverOffset: type === 'doughnut' || type === 'pie' ? 10 : 0,
                        borderRadius: type === 'bar' ? 6 : 0,
                        borderSkipped: type === 'bar' ? false : undefined
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: type !== 'bar',
                            position: 'bottom',
                            labels: {
                                boxWidth: 12,
                                padding: 10,
                                font: { size: 11, weight: '600' }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    return `${label}: ${value}`;
                                }
                            }
                        }
                    },
                    cutout: (type === 'doughnut') ? '65%' : undefined,
                    animation: {
                        animateRotate: true,
                        animateScale: true,
                        duration: 1500,
                        easing: 'easeOutQuart'
                    }
                }
            };
            
            // Configuración específica para gráficos de barras
            if (type === 'bar') {
                config.options.indexAxis = 'y';
                config.options.scales = {
                    x: {
                        beginAtZero: true,
                        grid: { display: true, color: 'rgba(0,0,0,0.05)' },
                        ticks: { font: { size: 11 } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { font: { size: 11, weight: '600' } }
                    }
                };
            }
            
            console.log(`  - Creando Chart para ${canvas.id}...`);
            new Chart(ctx, config);
            canvas.dataset.chartCreated = 'true';
            console.log(`  ✓ Chart creado exitosamente para ${canvas.id}`);
            
        } catch (e) {
            console.error(`Error creando gráfico para ${canvas.id}:`, e);
            console.error('  - data-labels:', canvas.dataset.labels);
            console.error('  - data-values:', canvas.dataset.values);
            console.error('  - data-type:', canvas.dataset.type);
            console.error('  - data-colors:', canvas.dataset.colors);
        }
    });
    
    console.log('Inicialización de gráficos completada');
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM cargado, esperando 100ms antes de inicializar gráficos...');
    setTimeout(initializeCharts, 100);
});
