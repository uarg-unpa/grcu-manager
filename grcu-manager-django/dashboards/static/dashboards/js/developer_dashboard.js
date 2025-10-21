// Developer Dashboard JavaScript
// This file contains the base functionality for the developer dashboard

// Function to initialize tooltips
function initializeDeveloperDashboardTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Function to create a doughnut chart
function createDeveloperDashboardChart(canvasId, orphanCount, relatedCount, colors) {
    var ctx = document.getElementById(canvasId);
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Huérfanos', 'Relacionados'],
                datasets: [{
                    data: [orphanCount, relatedCount],
                    backgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: { display: true, position: 'bottom' }
                },
                cutout: '65%'
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeDeveloperDashboardTooltips();
    // Charts will be initialized by inline script with dynamic data
});