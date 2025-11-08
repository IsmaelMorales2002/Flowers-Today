  document.addEventListener('DOMContentLoaded', function () {
    const botones = document.querySelectorAll('.btn-toggle-estado');
    const inputId = document.getElementById('modal-id-categoria');
    const inputAccion = document.getElementById('modal-accion-categoria');
    const mensaje = document.getElementById('modal-mensaje-estado');
    const nota = document.getElementById('modal-nota-estado');
    const btnAccion = document.getElementById('modal-btn-accion');

    botones.forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        const estado = btn.getAttribute('data-estado');
        const nombre = btn.getAttribute('data-nombre');

        inputId.value = id;
        inputAccion.value = estado;

        if (estado === 'desactivar') {
          mensaje.innerHTML = `¿Estás seguro que deseas <span class="text-danger fw-bold">desactivar</span> la categoría <strong>${nombre}</strong>?`;
          nota.innerHTML = `<div class="alert alert-danger border border-danger">
                              <i class="bi bi-exclamation-triangle-fill me-1"></i>
                              <strong>Nota:</strong> Los productos asociados no se mostrarán a los clientes.
                            </div>`;
        } else {
          mensaje.innerHTML = `¿Estás seguro que deseas <span class="text-success fw-bold">activar</span> la categoría <strong>${nombre}</strong>?`;
          nota.innerHTML = `<div class="alert alert-success border border-success">
                              <i class="bi bi-check-circle-fill me-1"></i>
                              <strong>Nota:</strong> Los productos asociados volverán a mostrarse a los clientes.
                            </div>`;
        }

        // Botón de acción mantiene color personalizado
        btnAccion.style.backgroundColor = '#6C2DC7';
      });
    });
  });

