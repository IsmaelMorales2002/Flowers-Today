document.addEventListener("DOMContentLoaded", () => {
  // Contenedor donde irán las cards
  const contenedor = document.getElementById("contenedor-productos");
  const titulo = document.getElementById('titulo-carrito')
  const resumen = document.getElementById('resumen-total')
  let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

  if (carrito.length === 0) {
    titulo.innerHTML = 'Carrito De Compras Vacio'
    return;
  }
  if (carrito.length != 0){
    titulo.innerHTML = 'Carrito De Compras'
    resumen.style.display = 'inline'
  }

  // Limpiar el contenedor
  contenedor.innerHTML = "";

  // Recorrer productos del carrito y crear las cards
  carrito.forEach(producto => {
    const card = document.createElement("div");
    card.classList.add("card", "mb-3", "shadow-sm");
    card.innerHTML = `
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-4 col-md-2">
            <img src="${producto.imagen || '/static/img/producto-default.png'}" 
                 alt="${producto.nombre}" 
                 class="img-thumbnail me-3" style="width: 90px;">
          </div>
          <div class="col-8 col-md-6">
            <h5 class="card-title">${producto.nombre}</h5>
            <p class="text-muted mb-0">${producto.descripcion}</p>
          </div>
          <div class="col-12 col-md-4 mt-3 mt-md-0">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <button class="btn btn-sm text-white btn-restar" style="background: #6C2DC7;">−</button>
                <span class="mx-2 cantidad">${producto.cantidad || 1}</span>
                <button class="btn btn-dark btn-sm btn-sumar">+</button>
              </div>
              <div class="text-end">
                <strong class="me-4 precio-unitario" data-precio="${producto.precio}">
                $${(producto.precio * (producto.cantidad || 1)).toFixed(2)}
                </strong>
                <button class="btn btn-danger btn-sm btn-eliminar" data-id="${producto.id}">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    contenedor.appendChild(card);
  });

  contenedor.addEventListener('click', (e) => {
    const btnSumar = e.target.closest('.btn-sumar')
    const btnRestar = e.target.closest('.btn-restar')

    if(btnSumar || btnRestar ){
        const card = e.target.closest('.card')
        const id = card.querySelector('.btn-eliminar').dataset.id
        const cantidadElemento = card.querySelector('.cantidad')
        const precioElemento = card.querySelector('.precio-unitario')

        const producto = carrito.find(p => p.id == id)

        let cantidad = parseInt(cantidadElemento.textContent)

        if(btnSumar)
            cantidad++
        else if(btnRestar && cantidad > 1)
            cantidad--
        
        cantidadElemento.textContent = cantidad;
        const nuevoPrecio = producto.precio * cantidad;
        precioElemento.textContent =`$${nuevoPrecio.toFixed(2)}`
    }
  })
});
