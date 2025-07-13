 document.addEventListener('DOMContentLoaded', function () {
    const modal = new bootstrap.Modal(document.getElementById('modalVerCliente'));
    const modalNombre = document.getElementById('modal-nombre');
    const modalCorreo = document.getElementById('modal-correo');
    const modalTelefono = document.getElementById('modal-telefono');
    const modalImagen = document.getElementById('modal-imagen');
    const modalEstado = document.getElementById('modal-estado');

    document.querySelectorAll('.btn-ver-cliente').forEach(btn => {
      btn.addEventListener('click', () => {
        const nombre = btn.getAttribute('data-nombre');
        const correo = btn.getAttribute('data-correo');
        const telefono = btn.getAttribute('data-telefono');
        const imagen = btn.getAttribute('data-imagen');
        const estado = btn.getAttribute('data-estado') === 'True';

        modalNombre.textContent = nombre;
        modalCorreo.textContent = correo;
        modalTelefono.textContent = telefono;
        modalImagen.src = imagen;

        modalEstado.textContent = estado ? 'Activo' : 'Inactivo';
        modalEstado.classList.remove('text-success', 'text-danger');
        modalEstado.classList.add(estado ? 'text-success' : 'text-danger');
      });
    });
});