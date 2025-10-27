  let modalDescripcion = document.getElementById('modalDescripcion');
  modalDescripcion.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget;
    let descripcion = button.getAttribute('data-descripcion');
    let modalBody = modalDescripcion.querySelector('#contenidoDescripcion');
    modalBody.textContent = descripcion;
  });

  document.addEventListener("DOMContentLoaded", function() {
    let modalComentario = document.getElementById('modalAgregarComentario');
    modalComentario.addEventListener('show.bs.modal', function (event) {
        let button = event.relatedTarget;
        let idServicio = button.getAttribute('data-id'); 
        let comentario = button.getAttribute('data-comentario');
        let validacion = button.getAttribute('data-validacion');

        // Llenar los campos del modal
        modalComentario.querySelector('#idServicioComentario').value = idServicio;
        modalComentario.querySelector('#comentarioAdmin').value = comentario || '';
        modalComentario.querySelector('#estadoUsuario').textContent = validacion || 'Pendiente';
    });
});