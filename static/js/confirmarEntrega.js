document.addEventListener("DOMContentLoaded", function () {
  let idSeleccionado = null;

  // Detecta click en cualquier botón de entrega
  document.querySelectorAll(".btn-confirmar-entrega").forEach((btn) => {
    btn.addEventListener("click", function () {
      idSeleccionado = this.getAttribute("data-id");
      let modal = new bootstrap.Modal(document.getElementById("modalConfirmarEntrega"));
      modal.show();
    });
  });

  // Cuando el usuario confirma en el modal
  document.getElementById("btnConfirmarEntrega").addEventListener("click", function () {
    if (idSeleccionado) {
      document.getElementById(`form-entrega-${idSeleccionado}`).submit();
    }
  });
});
