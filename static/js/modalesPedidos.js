  let modalDescripcion = document.getElementById('modalDescripcion');
  modalDescripcion.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget;
    let descripcion = button.getAttribute('data-descripcion');
    let modalBody = modalDescripcion.querySelector('#contenidoDescripcion');
    modalBody.textContent = descripcion;
  });

document.addEventListener("DOMContentLoaded", function() {
    let modalComentario = document.getElementById('modalAgregarComentario');
    modalComentario.addEventListener('show.bs.modal', function(event) {
        let button = event.relatedTarget;
        let idServicio = button.getAttribute('data-id'); 
        let comentario = button.getAttribute('data-comentario') || '';

        // Elementos del modal
        let botonGuardar = modalComentario.querySelector('button[type="submit"]');
        let textareaComentario = modalComentario.querySelector('#comentarioAdmin');
        let estadoElemento = modalComentario.querySelector('#estadoUsuario');

        // Detectar True o False en el comentario
        let estadoTexto = 'Pendiente';
        let colorEstado = 'black'; // color por defecto

        if (comentario.includes('True')) {
            estadoTexto = 'Aceptado';
            colorEstado = 'green';
            comentario = comentario.replace('True', '').trim();
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
        } else if (comentario.includes('False')) {
            estadoTexto = 'Rechazado';
            colorEstado = 'red';
            comentario = comentario.replace('False', '').trim();
            botonGuardar.disabled = true;
            textareaComentario.disabled = true;
        } else {
            estadoTexto = 'Pendiente';
            colorEstado = 'black';
            botonGuardar.disabled = false;
            textareaComentario.disabled = false;
        }

        // Llenar los campos del modal
        modalComentario.querySelector('#idServicioComentario').value = idServicio;
        textareaComentario.value = comentario;
        estadoElemento.textContent = estadoTexto;
        estadoElemento.style.color = colorEstado; 
    });
});

