let modalDescripcion = document.getElementById('modalDescripcion');
modalDescripcion.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget;
    let descripcion = button.getAttribute('data-descripcion');
    let cantidad = button.getAttribute('data-cantidad');
    console.log(cantidad)
    let modalBody = modalDescripcion.querySelector('#contenidoDescripcion');
    let modalcantidad = modalDescripcion.querySelector('#cantidadSolicitada');
    modalBody.textContent = descripcion;
    modalcantidad.textContent = cantidad;
});

document.addEventListener("DOMContentLoaded", function () {
    let modalComentario = document.getElementById('modalAgregarComentario');

    modalComentario.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget;
        let idServicio = button.getAttribute('data-id');
        let comentario = button.getAttribute('data-comentario') || '';

        // Elementos del modal
        let botonGuardar = modalComentario.querySelector('button[type="submit"]');
        let textareaComentario = modalComentario.querySelector('#comentarioAdmin');
        let estadoElemento = modalComentario.querySelector('#estadoUsuario');

        // Remover cualquier aparición de true o false sin afectar el resto
        let comentarioLimpio = comentario.replace(/True|False/gi, '').trim();

        let estadoTexto = 'Pendiente';
        let colorEstado = 'black';

        if (/true/i.test(comentario)) {
            estadoTexto = 'Aceptado';
            colorEstado = 'green';
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
        } else if (/false/i.test(comentario)) {
            estadoTexto = 'Rechazado';
            colorEstado = 'red';
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
        } else {
            estadoTexto = 'Pendiente';
            colorEstado = 'black';
            botonGuardar.disabled = false;
            textareaComentario.disabled = false;
        }

        // Rellenar los datos en el modal
        modalComentario.querySelector('#idServicioComentario').value = idServicio;
        textareaComentario.value = comentarioLimpio;
        estadoElemento.textContent = estadoTexto;
        estadoElemento.style.color = colorEstado;
    });
});
