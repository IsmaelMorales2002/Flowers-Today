document.addEventListener("DOMContentLoaded", () => {
    const modal = new bootstrap.Modal(document.getElementById("modalExitoCompra"));
    modal.show();
    localStorage.removeItem('carrito')
});