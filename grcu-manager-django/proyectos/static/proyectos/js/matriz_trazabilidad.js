document.addEventListener('DOMContentLoaded', function() {
    const filtrosForm = document.getElementById('filtrosForm');
    if (!filtrosForm) return;

    const autoSubmitFields = ['tipo_req', 'estado_req', 'solo_huerfanos', 'solo_sin_cubrir'];

    autoSubmitFields.forEach(fieldId => {
        const el = document.getElementById(fieldId);
        if (!el) return;
        el.addEventListener('change', function() {
            filtrosForm.submit();
        });
    });
});
