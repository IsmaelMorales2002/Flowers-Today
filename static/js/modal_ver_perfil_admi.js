document.addEventListener('DOMContentLoaded', function () {
  const modalNombre = document.getElementById('modal-nombre');
  const modalCorreo = document.getElementById('modal-correo');
  const modalTelefono = document.getElementById('modal-telefono');
  const modalImagen = document.getElementById('modal-imagen');
  const modalEstado = document.getElementById('modal-estado');

  // Delegación de eventos usando jQuery para que funcione en móviles
  $(document).on('click', '.btn-ver-admi', function () {
    const $btn = $(this);
    const nombre = $btn.data('nombre');
    const correo = $btn.data('correo');
    const telefono = $btn.data('telefono');
    const imagen = $btn.data('imagen');
    const estado = $btn.data('estado') === true || $btn.data('estado') === 'True';

    modalNombre.textContent = nombre;
    modalCorreo.textContent = correo;
    modalTelefono.textContent = telefono;
    modalImagen.src = imagen;

    modalEstado.textContent = estado ? 'Activo' : 'Inactivo';
    modalEstado.classList.remove('text-success', 'text-danger');
    modalEstado.classList.add(estado ? 'text-success' : 'text-danger');
  });
});
