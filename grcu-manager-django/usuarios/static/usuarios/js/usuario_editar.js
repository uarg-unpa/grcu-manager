document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript de usuario_editar cargado correctamente');

    // Manejo de selección de roles con radio buttons
    const rolesBadges = document.querySelectorAll('.roles-badge');
    console.log('Encontrados', rolesBadges.length, 'badges de roles');

    // Inicializar estilos para roles ya seleccionados
    rolesBadges.forEach((badge, index) => {
        const radio = badge.querySelector('input[type="radio"]');
        const checkIcon = badge.querySelector('.rol-check-icon');
        const rolColor = badge.dataset.rolColor;

        console.log(`Badge ${index}: color=${rolColor}, checked=${radio?.checked}`);

        if (radio && radio.checked) {
            badge.classList.add('selected');
            if (rolColor) {
                badge.style.backgroundColor = rolColor;
            }
            if (checkIcon) {
                checkIcon.style.display = 'flex';
            }
            console.log(`Badge ${index}: estado inicial aplicado`);
        }
    });

    rolesBadges.forEach(badge => {
        badge.addEventListener('click', function(e) {
            console.log(`Click en badge ${Array.from(rolesBadges).indexOf(badge)}`);

            // Evitar que el evento se propague si se hace click en el input
            if (e.target.tagName === 'INPUT') return;

            // Marcar este radio button y desmarcar los demás
            rolesBadges.forEach(otherBadge => {
                const otherRadio = otherBadge.querySelector('input[type="radio"]');
                const otherCheckIcon = otherBadge.querySelector('.rol-check-icon');
                const otherRolColor = otherBadge.dataset.rolColor;

                if (otherBadge === badge) {
                    // Este es el badge seleccionado
                    otherRadio.checked = true;
                    otherBadge.classList.add('selected');
                    if (otherRolColor) {
                        otherBadge.style.backgroundColor = otherRolColor;
                    } else {
                        // Para "sin rol asignado"
                        otherBadge.style.backgroundColor = '';
                    }
                    if (otherCheckIcon) otherCheckIcon.style.display = 'flex';
                } else {
                    // Desmarcar los demás
                    otherRadio.checked = false;
                    otherBadge.classList.remove('selected');
                    otherBadge.style.backgroundColor = '';
                    if (otherCheckIcon) otherCheckIcon.style.display = 'none';
                }
            });
        });
    });

    // Manejar el toggle de estado activo
    const activeToggle = document.querySelector('.active-status-toggle');
    if (activeToggle) {
        const checkbox = activeToggle.querySelector('input[type="checkbox"]');
        const statusText = activeToggle.querySelector('.active-status-text');

        // Función para actualizar el estado visual
        function updateActiveStatus() {
            if (checkbox.checked) {
                activeToggle.classList.add('active');
                statusText.textContent = 'Sí, activo';
            } else {
                activeToggle.classList.remove('active');
                statusText.textContent = 'No, inactivo';
            }
        }

        // Actualizar estado inicial
        updateActiveStatus();

        activeToggle.addEventListener('click', function(e) {
            if (e.target.tagName !== 'INPUT') {
                checkbox.checked = !checkbox.checked;
            }

            // Actualizar el estado visual
            updateActiveStatus();
        });
    }
});