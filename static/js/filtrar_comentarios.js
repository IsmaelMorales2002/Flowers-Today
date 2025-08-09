document.addEventListener('DOMContentLoaded', function () {
    const filtroTexto = document.getElementById('searchInput');
    const filtroDesde = document.getElementById('startDate');
    const filtroHasta = document.getElementById('endDate');
    const btnLimpiar = document.getElementById('clearFilters');
    const comentarios = document.querySelectorAll('.comentario-item');

    function filtrar() {
        const texto = filtroTexto.value.toLowerCase();
        const desde = filtroDesde.value ? new Date(filtroDesde.value) : null;
        const hasta = filtroHasta.value ? new Date(filtroHasta.value) : null;

        comentarios.forEach(comentario => {
            const textoComentario = comentario.dataset.texto.toLowerCase();
            const usuarioComentario = comentario.dataset.usuario.toLowerCase();
            const fechaComentario = new Date(comentario.dataset.fecha);

            let visible = true;

            // Filtro por texto general (comentario o usuario)
            if (texto && !textoComentario.includes(texto) && !usuarioComentario.includes(texto)) {
                visible = false;
            }

            // Filtro por fecha desde
            if (desde && fechaComentario < desde) {
                visible = false;
            }

            // Filtro por fecha hasta
            if (hasta && fechaComentario > hasta) {
                visible = false;
            }

            comentario.style.display = visible ? '' : 'none';
        });
    }

    filtroTexto.addEventListener('input', filtrar);
    filtroDesde.addEventListener('change', filtrar);
    filtroHasta.addEventListener('change', filtrar);

    btnLimpiar.addEventListener('click', () => {
        filtroTexto.value = '';
        filtroDesde.value = '';
        filtroHasta.value = '';
        filtrar();
    });
});
