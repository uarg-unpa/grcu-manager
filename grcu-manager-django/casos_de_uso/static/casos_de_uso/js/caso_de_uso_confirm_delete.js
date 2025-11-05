document.addEventListener('DOMContentLoaded', function() {
    const confirmInput = document.getElementById('confirmText');
    const deleteBtn = document.getElementById('deleteBtn');
    // El valor esperado debe ser inyectado desde el template
    const expectedText = window.CASO_NOMBRE || '';
    
    function validateConfirmation() {
        const inputValue = confirmInput.value.trim();
        const isValid = inputValue === expectedText;
        deleteBtn.disabled = !isValid;
        if (isValid) {
            deleteBtn.classList.remove('btn-danger');
            deleteBtn.classList.add('btn-outline-danger');
        } else {
            deleteBtn.classList.remove('btn-outline-danger');
            deleteBtn.classList.add('btn-danger');
        }
    }
    confirmInput.addEventListener('input', validateConfirmation);
    document.getElementById('deleteForm').addEventListener('submit', function(e) {
        const inputValue = confirmInput.value.trim();
        if (inputValue !== expectedText) {
            e.preventDefault();
            alert('El texto de confirmación no coincide. Por favor, escribe exactamente: "' + expectedText + '"');
            confirmInput.focus();
        }
    });
});
