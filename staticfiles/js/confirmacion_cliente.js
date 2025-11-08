  document.addEventListener('DOMContentLoaded', () => {
    const btnAbrirModal = document.getElementById('btn-confirmar-actualizacion');
    const btnConfirmarGuardar = document.getElementById('btn-confirmar-guardar');
    const formEditar = document.getElementById('form-editar-perfil');
    const modal = new bootstrap.Modal(document.getElementById('modalConfirmarActualizacion'));

    // Al hacer clic en “Guardar Cambios”, mostrar el modal
    btnAbrirModal.addEventListener('click', (e) => {
      e.preventDefault();
      modal.show();
    });

    // Si confirma, enviar el formulario
    btnConfirmarGuardar.addEventListener('click', () => {
      modal.hide();
      formEditar.submit();
    });
  });