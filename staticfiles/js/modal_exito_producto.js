document.addEventListener('DOMContentLoaded', function () {
  const modalElementProducto = document.getElementById('modalCreadoExitoProducto');
  if (modalElementProducto) {
    const modalProducto = new bootstrap.Modal(modalElementProducto);
    modalProducto.show();
  }
});
