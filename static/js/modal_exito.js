document.addEventListener('DOMContentLoaded', function () {
  const modalElement = document.getElementById('modalExito');
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  }
});
