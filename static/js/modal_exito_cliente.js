document.addEventListener('DOMContentLoaded', function () {
  const modalElementCliente = document.getElementById('modalCreadoExitoCliente');
  if (modalElementCliente) {
    const modalCliente = new bootstrap.Modal(modalElementCliente);
    modalCliente.show();
  }
});
