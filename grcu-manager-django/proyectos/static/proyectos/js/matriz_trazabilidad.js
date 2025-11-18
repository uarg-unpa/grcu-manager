document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit de filtros
    const filtrosForm = document.getElementById('filtrosForm');
    if (filtrosForm) {
        const autoSubmitFields = ['tipo_req', 'estado_req', 'solo_huerfanos', 'solo_sin_cubrir'];
        autoSubmitFields.forEach(fieldId => {
            const el = document.getElementById(fieldId);
            if (!el) return;
            el.addEventListener('change', function() {
                filtrosForm.submit();
            });
        });
    }

    // ===== TOOLTIPS INTERACTIVOS =====
    
    // Crear el elemento de tooltip una sola vez
    const tooltip = document.createElement('div');
    tooltip.className = 'matriz-tooltip';
    tooltip.style.display = 'none';
    document.body.appendChild(tooltip);

    let tooltipTimeout;

    // Función para mostrar tooltip
    function showTooltip(content, x, y) {
        clearTimeout(tooltipTimeout);
        tooltip.innerHTML = content;
        tooltip.style.display = 'block';
        
        // Posicionar el tooltip
        const tooltipRect = tooltip.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        // Ajustar posición X (evitar salirse del viewport)
        let finalX = x + 10;
        if (finalX + tooltipRect.width > viewportWidth - 20) {
            finalX = x - tooltipRect.width - 10;
        }
        
        // Ajustar posición Y
        let finalY = y + 10;
        if (finalY + tooltipRect.height > viewportHeight - 20) {
            finalY = y - tooltipRect.height - 10;
        }
        
        tooltip.style.left = finalX + 'px';
        tooltip.style.top = finalY + 'px';
        
        // Animación de entrada
        tooltip.style.opacity = '0';
        setTimeout(() => {
            tooltip.style.opacity = '1';
        }, 10);
    }

    function hideTooltip() {
        tooltipTimeout = setTimeout(() => {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                tooltip.style.display = 'none';
            }, 200);
        }, 100);
    }

    // ===== TOOLTIPS PARA REQUERIMIENTOS =====
    document.querySelectorAll('.req-nombre').forEach(reqElement => {
        const link = reqElement.closest('a');
        const isHuerfano = link.classList.contains('req-huerfano');
        
        reqElement.addEventListener('mouseenter', function(e) {
            const reqNombre = this.textContent.trim();
            const row = this.closest('tr');
            const estadoBadge = row.querySelector('.badge');
            const estadoTexto = estadoBadge ? estadoBadge.textContent.trim() : 'Sin estado';
            
            // Contar relaciones (checkmarks en la fila)
            const relacionados = row.querySelectorAll('.relacionado').length;
            const totalCasos = row.querySelectorAll('.celda-relacion').length;
            
            const content = `
                <div class="tooltip-header ${isHuerfano ? 'tooltip-warning' : 'tooltip-primary'}">
                    <i class="bi ${isHuerfano ? 'bi-exclamation-triangle-fill' : 'bi-file-text-fill'}"></i>
                    <strong>Requerimiento</strong>
                </div>
                <div class="tooltip-body">
                    <div class="tooltip-title">${reqNombre}</div>
                    <div class="tooltip-item">
                        <i class="bi bi-circle-fill"></i>
                        <span>Estado: <strong>${estadoTexto}</strong></span>
                    </div>
                    <div class="tooltip-item">
                        <i class="bi bi-diagram-3"></i>
                        <span>Casos de uso: <strong>${relacionados}/${totalCasos}</strong></span>
                    </div>
                    ${isHuerfano ? '<div class="tooltip-warning-text"><i class="bi bi-exclamation-circle"></i> Sin casos de uso asociados</div>' : ''}
                </div>
            `;
            
            showTooltip(content, e.pageX, e.pageY);
        });
        
        reqElement.addEventListener('mouseleave', hideTooltip);
        
        reqElement.addEventListener('mousemove', function(e) {
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY + 10) + 'px';
        });
    });

    // ===== TOOLTIPS PARA CASOS DE USO (headers) =====
    document.querySelectorAll('.caso-header').forEach(casoHeader => {
        const isHuerfano = casoHeader.classList.contains('caso-huerfano');
        const casoNombre = casoHeader.getAttribute('data-nombre');
        
        casoHeader.addEventListener('mouseenter', function(e) {
            const casoIndex = Array.from(this.parentElement.children).indexOf(this) - 2; // -2 por las 2 primeras columnas
            
            // Contar requerimientos relacionados (columna vertical)
            const rows = document.querySelectorAll('.matriz-table tbody tr');
            let relacionados = 0;
            rows.forEach(row => {
                const cells = row.querySelectorAll('.celda-relacion');
                if (cells[casoIndex] && cells[casoIndex].classList.contains('relacionado')) {
                    relacionados++;
                }
            });
            
            const content = `
                <div class="tooltip-header ${isHuerfano ? 'tooltip-warning' : 'tooltip-success'}">
                    <i class="bi ${isHuerfano ? 'bi-exclamation-triangle-fill' : 'bi-diagram-3-fill'}"></i>
                    <strong>Caso de Uso</strong>
                </div>
                <div class="tooltip-body">
                    <div class="tooltip-title">${casoNombre}</div>
                    <div class="tooltip-item">
                        <i class="bi bi-list-check"></i>
                        <span>Requerimientos: <strong>${relacionados}/${rows.length}</strong></span>
                    </div>
                    ${isHuerfano ? '<div class="tooltip-warning-text"><i class="bi bi-exclamation-circle"></i> Sin requerimientos asociados</div>' : ''}
                    <div class="tooltip-action">
                        <i class="bi bi-hand-index"></i> Click para ver detalles
                    </div>
                </div>
            `;
            
            showTooltip(content, e.pageX, e.pageY);
        });
        
        casoHeader.addEventListener('mouseleave', hideTooltip);
    });

    // ===== EFECTOS PARA CELDAS DE RELACIÓN =====
    document.querySelectorAll('.celda-relacion').forEach(celda => {
        celda.addEventListener('mouseenter', function() {
            const row = this.closest('tr');
            const cellIndex = Array.from(row.children).indexOf(this);
            
            // Highlight de fila completa
            row.classList.add('row-highlight');
            
            // Highlight de columna completa
            document.querySelectorAll('.matriz-table tbody tr').forEach(r => {
                const cell = r.children[cellIndex];
                if (cell) cell.classList.add('col-highlight');
            });
            
            // Highlight del header
            const headers = document.querySelectorAll('.matriz-table thead th');
            if (headers[cellIndex]) {
                headers[cellIndex].classList.add('header-highlight');
            }
        });
        
        celda.addEventListener('mouseleave', function() {
            // Quitar todos los highlights
            document.querySelectorAll('.row-highlight').forEach(el => el.classList.remove('row-highlight'));
            document.querySelectorAll('.col-highlight').forEach(el => el.classList.remove('col-highlight'));
            document.querySelectorAll('.header-highlight').forEach(el => el.classList.remove('header-highlight'));
        });
    });

    // ===== ANIMACIÓN AL SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.matriz-table tbody tr').forEach(row => {
        observer.observe(row);
    });

    // ===== BÚSQUEDA RÁPIDA EN MATRIZ =====
    const searchInput = document.getElementById('matriz-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.matriz-table tbody tr');
            
            rows.forEach(row => {
                const reqNombre = row.querySelector('.req-nombre').textContent.toLowerCase();
                if (reqNombre.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // ===== ESTADÍSTICAS EN TIEMPO REAL AL HOVER =====
    let estadisticasTimeout;
    document.querySelectorAll('.celda-relacion.relacionado').forEach(celda => {
        celda.addEventListener('mouseenter', function() {
            clearTimeout(estadisticasTimeout);
            estadisticasTimeout = setTimeout(() => {
                // Podría mostrar estadísticas adicionales aquí
                this.style.transform = 'scale(1.3)';
            }, 300);
        });
        
        celda.addEventListener('mouseleave', function() {
            clearTimeout(estadisticasTimeout);
            this.style.transform = 'scale(1)';
        });
    });
});
