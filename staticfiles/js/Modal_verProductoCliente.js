// static/js/Modal_verProductoCliente.js
document.addEventListener("DOMContentLoaded", () => {
  const modalEl = document.getElementById("modalVerProductoCliente");
  if (!modalEl) return;

  const bsModal = new bootstrap.Modal(modalEl);

  const elImg   = document.getElementById("modal-imagen-producto");
  const elCat   = document.getElementById("modal-categoria");
  const elNom   = document.getElementById("modal-nombre-producto");
  const elDesc  = document.getElementById("modal-descripcion");
  const elExi   = document.getElementById("modal-existencias");
  const elPrec  = document.getElementById("modal-precio");
  const elTipo  = document.getElementById("modal-tipo-producto");

  const defaultImg = modalEl.dataset.defaultImg || "";

  // Delegación: cualquier click en .btn-verProducto
  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".btn-verProducto");
    if (!btn) return;

    const data = {
      categoria:   btn.dataset.categoria || "—",
      nombre:      btn.dataset.nombre || "Producto",
      descripcion: btn.dataset.descripcion || "Sin descripción",
      existencias: btn.dataset.existencias ?? "—",
      precio:      btn.dataset.precio ?? "0",
      tipo:        btn.dataset.tipo || "—",
      imagen:      btn.dataset.imagen || defaultImg
    };

    // Llenar campos
    elCat.textContent  = data.categoria;
    elNom.textContent  = data.nombre;
    elDesc.textContent = data.descripcion;
    elExi.textContent  = data.existencias;
    elPrec.textContent = Number(data.precio).toFixed(2);
    elTipo.textContent = data.tipo;

    elImg.src = data.imagen || defaultImg;
    elImg.alt = data.nombre;
    elImg.onerror = () => { elImg.src = defaultImg; };

    // Mostrar modal
    bsModal.show();
  });
});
