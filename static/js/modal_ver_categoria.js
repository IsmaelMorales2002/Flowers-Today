 document.addEventListener('DOMContentLoaded', function () {
    const modal = new bootstrap.Modal(document.getElementById('modalVerCategoria'));
    const modalNombre = document.getElementById('modal-nombre');
    const modalEstado = document.getElementById('modal-estado');

    document.querySelectorAll('.btn-ver-categoria').forEach(btn => {
      btn.addEventListener('click', () => {
        const nombre = btn.getAttribute('data-nombre');
        const estado = btn.getAttribute('data-estado') === 'True';

        modalNombre.textContent = nombre;

        modalEstado.textContent = estado ? 'Activo' : 'Inactivo';
        modalEstado.classList.remove('text-success', 'text-danger');
        modalEstado.classList.add(estado ? 'text-success' : 'text-danger');
      });
    });
});