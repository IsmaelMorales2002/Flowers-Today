$(document).ready(function () {
  const inputId = $('#modal-id-usuario');
  const inputAccion = $('#modal-accion-usuario');
  const mensaje = $('#modal-mensaje-estado');
  const nota = $('#modal-nota-estado');
  const btnAccion = $('#modal-btn-accion');
  const modalBootstrap = new bootstrap.Modal(document.getElementById('modalToggleEstado'));

  // Delegar evento para botones dinámicos dentro de la tabla
  $('#tabla-admi').on('click', '.btn-toggle-estado', function (event) {
    event.preventDefault();

    const btn = $(this);
    const id = btn.data('id');
    const estado = btn.data('estado');
    const nombre = btn.data('nombre');

    inputId.val(id);
    inputAccion.val(estado);

    if (estado === 'desactivar') {
      mensaje.html(`¿Estás seguro que deseas <span class="text-danger fw-bold">desactivar</span> al administrador <strong>${nombre}</strong>?`);
      nota.html(`<div class="alert alert-danger border border-danger">
                  <i class="bi bi-exclamation-triangle-fill me-1"></i>
                  <strong>Nota:</strong> El administrador no podrá acceder al sistema.
                </div>`);
    } else {
      mensaje.html(`¿Estás seguro que deseas <span class="text-success fw-bold">activar</span> al administrador <strong>${nombre}</strong>?`);
      nota.html(`<div class="alert alert-success border border-success">
                  <i class="bi bi-check-circle-fill me-1"></i>
                  <strong>Nota:</strong> El administrador podrá acceder al sistema nuevamente.
                </div>`);
    }

    btnAccion.css('background-color', '#6C2DC7');

    modalBootstrap.show();
  });
});
