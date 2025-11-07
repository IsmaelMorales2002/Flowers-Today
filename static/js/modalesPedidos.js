let modalDescripcion = document.getElementById('modalDescripcion');

modalDescripcion.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget;
    let descripcion = button.getAttribute('data-descripcion');
    let cantidad = button.getAttribute('data-cantidad');

    let modalBody = modalDescripcion.querySelector('#contenidoDescripcion');
    let modalCantidad = modalDescripcion.querySelector('#cantidadSolicitada');

    modalBody.textContent = descripcion;
    modalCantidad.textContent = cantidad;
});


document.addEventListener("DOMContentLoaded", function () {
    let modalComentario = document.getElementById('modalAgregarComentario');

    modalComentario.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget;
        let idServicio = button.getAttribute('data-id');
        let comentario = button.getAttribute('data-comentario') || '';
        let precio = button.getAttribute('data-precio') || ''; // <-- nuevo atributo

        // Elementos del modal
        let botonGuardar = modalComentario.querySelector('button[type="submit"]');
        let textareaComentario = modalComentario.querySelector('#comentarioAdmin');
        let estadoElemento = modalComentario.querySelector('#estadoUsuario');
        let inputPrecio = modalComentario.querySelector('#precioServicio');

        // Remover cualquier aparición de true o false sin afectar el resto
        let comentarioLimpio = comentario.replace(/True|False/gi, '').trim();

        let estadoTexto = 'Pendiente';
        let colorEstado = 'black';

        // Validar estado del comentario
        if (/true/i.test(comentario)) {
            estadoTexto = 'Aceptado';
            colorEstado = 'green';
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
            inputPrecio.disabled = true;
        } else if (/false/i.test(comentario)) {
            estadoTexto = 'Rechazado';
            colorEstado = 'red';
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
            inputPrecio.disabled = true;
        } else {
            estadoTexto = 'Pendiente';
            colorEstado = 'black';
            botonGuardar.disabled = false;
            textareaComentario.disabled = false;
        }

        // Rellenar datos
        modalComentario.querySelector('#idServicioComentario').value = idServicio;
        textareaComentario.value = comentarioLimpio;
        estadoElemento.textContent = estadoTexto;
        estadoElemento.style.color = colorEstado;

        // Manejar el precio
        if (precio && parseFloat(precio) > 0) {
            inputPrecio.value = precio;
            inputPrecio.disabled = true; // Bloquear si ya tiene precio
        } else {
            inputPrecio.value = ''; // Vacío si no tiene
            inputPrecio.disabled = false; // Permitir escribir
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modalGestionar');
  modal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const servicioId = button.getAttribute('data-id');
    document.getElementById('id_servicio_rechazar').value = servicioId;
  });
});

