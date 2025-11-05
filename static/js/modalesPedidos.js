document.addEventListener("DOMContentLoaded", function () {
    let modalComentario = document.getElementById('modalAgregarComentario');

    modalComentario.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget;
        let idServicio = button.getAttribute('data-id');
        let comentario = button.getAttribute('data-comentario') || '';
        let precio = button.getAttribute('data-precio') || '';

        // Elementos del modal
        let botonGuardar = modalComentario.querySelector('button[type="submit"]');
        let textareaComentario = modalComentario.querySelector('#comentarioAdmin');
        let estadoElemento = modalComentario.querySelector('#estadoUsuario');
        let inputPrecio = modalComentario.querySelector('#precioServicio');

        // Limpieza del comentario
        let comentarioLimpio = comentario.replace(/True|False/gi, '').trim();

        // Determinar estado y color
        let estadoTexto = 'Pendiente';
        let colorEstado = 'black';

        // Detectar si ya está aprobado o rechazado
        if (/true/i.test(comentario)) {
            estadoTexto = 'Aceptado';
            colorEstado = 'green';
        } else if (/false/i.test(comentario)) {
            estadoTexto = 'Rechazado';
            colorEstado = 'red';
        }

        // Si el servicio ya tiene comentario o precio asignado, deshabilitar edición
        let tieneComentario = comentarioLimpio !== '';
        let tienePrecio = precio && parseFloat(precio) > 0;

        if (tieneComentario || tienePrecio || estadoTexto !== 'Pendiente') {
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
            inputPrecio.disabled = true;
        } else {
            botonGuardar.disabled = false;
            textareaComentario.disabled = false;
            inputPrecio.disabled = false;
        }

        // Rellenar los datos en el modal
        modalComentario.querySelector('#idServicioComentario').value = idServicio;
        textareaComentario.value = comentarioLimpio;
        inputPrecio.value = tienePrecio ? parseFloat(precio).toFixed(2) : '';
        estadoElemento.textContent = estadoTexto;
        estadoElemento.style.color = colorEstado;
    });
});
