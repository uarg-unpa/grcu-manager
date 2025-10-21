document.addEventListener('DOMContentLoaded', function() {
    const setBadgeState = (badge, isChecked) => {
        badge.classList.toggle('active', isChecked);
        badge.classList.toggle('inactive', !isChecked);
        badge.setAttribute('aria-checked', isChecked);
    };

    document.querySelectorAll('.roles-badge').forEach(badge => {
        const checkbox = badge.querySelector('input[type="checkbox"]');
        badge.setAttribute('role', 'checkbox');
        badge.setAttribute('tabindex', '0');

        // Aplicar estado inicial basado en si el checkbox está marcado
        setBadgeState(badge, checkbox.checked);

        badge.addEventListener('click', function(event) {
            event.preventDefault();
            checkbox.checked = !checkbox.checked;
            setBadgeState(badge, checkbox.checked);
        });

        badge.addEventListener('keydown', function(event) {
            if (event.key === ' ' || event.key === 'Enter') {
                event.preventDefault();
                checkbox.checked = !checkbox.checked;
                setBadgeState(badge, checkbox.checked);
            }
        });
    });

    // Manejar el toggle del estado activo
    const activeToggle = document.querySelector('.active-status-toggle');
    if (activeToggle) {
        const checkbox = activeToggle.querySelector('input[type="checkbox"]');
        const textElement = activeToggle.querySelector('.active-status-text');

        const updateToggleText = () => {
            textElement.textContent = checkbox.checked ? 'Sí, activo' : 'No, inactivo';
        };

        // Aplicar estado inicial
        updateToggleText();

        activeToggle.addEventListener('click', function(event) {
            event.preventDefault();
            checkbox.checked = !checkbox.checked;
            updateToggleText();
        });

        activeToggle.addEventListener('keydown', function(event) {
            if (event.key === ' ' || event.key === 'Enter') {
                event.preventDefault();
                checkbox.checked = !checkbox.checked;
                updateToggleText();
            }
        });
    }
});