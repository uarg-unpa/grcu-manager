let versionSeleccionada = null;

function seleccionarParaComparar(historyId, numeroVersion) {
    versionSeleccionada = historyId;
    document.getElementById('versionSeleccionada').textContent = 'Versión #' + numeroVersion;
    // Limpiar lista
    const lista = document.getElementById('listaVersiones');
    lista.innerHTML = '';
    // Obtener todas las versiones menos la seleccionada
    window.VERSIONES.forEach(function(item) {
        if (item.history_id !== historyId) {
            const btn = document.createElement('button');
            btn.className = 'list-group-item list-group-item-action';
            btn.innerHTML = `<strong>Versión #${item.numero}</strong> - ${item.fecha}`;
            btn.onclick = function() {
                compararVersiones(item.history_id);
            };
            lista.appendChild(btn);
        }
    });
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('compararModal'));
    modal.show();
}

function compararVersiones(version2Id) {
    const url = window.COMPARAR_URL +
                '?version1_id=' + versionSeleccionada + '&version2_id=' + version2Id;
    window.location.href = url;
}
