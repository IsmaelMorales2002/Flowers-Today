  document.addEventListener('DOMContentLoaded', () => {
    const btnAbrirModal = document.getElementById('btn-confirmar-actualizacion-admin');
    const btnConfirmarGuardar = document.getElementById('btn-confirmar-guardar-admin');
    const formEditar = document.getElementById('form-editar-perfil');
    const modal = new bootstrap.Modal(document.getElementById('modalConfirmarActualizacionAdmin'));

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