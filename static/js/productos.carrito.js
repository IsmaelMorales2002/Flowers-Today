document.addEventListener("DOMContentLoaded", () => {
  const contenedor = document.getElementById("contenedor-productos");
  const titulo = document.getElementById('titulo-carrito');
  const resumen = document.getElementById('resumen-total');
  let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

  if (carrito.length === 0) {
    titulo.innerHTML = 'Carrito De Compras Vacío';
    return;
  } else {
    titulo.innerHTML = 'Carrito De Compras';
    resumen.style.display = 'inline';
  }

  // Limpiar el contenedor
  contenedor.innerHTML = "";

  // Crear cards
  carrito.forEach(producto => {
    const card = document.createElement("div");
    card.classList.add("card", "mb-3", "shadow-sm");
    card.innerHTML = `
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-4 col-md-2">
            <img src="${producto.imagen || '/static/img/producto-default.png'}" 
                 alt="${producto.nombre}" class="img-thumbnail me-3" style="width: 90px;">
          </div>
          <div class="col-8 col-md-5">
            <h5 class="card-title">${producto.nombre}</h5>
            <p class="text-muted mb-0">${producto.descripcion}</p>
          </div>
          <div class="col-12 col-md-5 mt-3 mt-md-0">
            <div class="row text-center">
              <div class="col-4">
                <span class="fw-bold d-block mb-1">Cantidad</span>
                <div class="d-flex justify-content-center align-items-center">
                  <button class="btn btn-sm btn-dark text-white btn-restar">−</button>
                  <span class="mx-2 cantidad">${producto.cantidad || 1}</span>
                  <button class="btn btn-sm btn-sumar text-white" style="background: #6C2DC7;">+</button>
                </div>
              </div>
              <div class="col-4">
                <span class="fw-bold d-block mb-1">Total</span>
                <strong class="precio-unitario" data-precio="${producto.precio}">
                  $${(producto.precio * (producto.cantidad || 1)).toFixed(2)}
                </strong>
              </div>
              <div class="col-4">
                <span class="fw-bold d-block mb-1">Eliminar</span>
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

  // Click en botones de sumar, restar y eliminar
  contenedor.addEventListener('click', (e) => {
    const btnSumar = e.target.closest('.btn-sumar');
    const btnRestar = e.target.closest('.btn-restar');
    const btnEliminar = e.target.closest('.btn-eliminar');

    if(btnEliminar){
      const id = btnEliminar.dataset.id;
      carrito = carrito.filter(item => item.id !== id);
      localStorage.setItem('carrito', JSON.stringify(carrito));

      const card = btnEliminar.closest('.card');
      if(card) card.remove();

      if(carrito.length === 0){
        resumen.remove();
        titulo.innerHTML = 'Carrito De Compras Vacío';
      }
      ActualizarPrecios();
    }

    if(btnSumar || btnRestar){
      const card = e.target.closest('.card');
      const id = card.querySelector('.btn-eliminar').dataset.id;
      const cantidadElemento = card.querySelector('.cantidad');
      const precioElemento = card.querySelector('.precio-unitario');
      const producto = carrito.find(p => p.id == id);

      let cantidad = parseInt(cantidadElemento.textContent);
      if(btnSumar) cantidad++;
      else if(btnRestar && cantidad > 1) cantidad--;

      cantidadElemento.textContent = cantidad;
      precioElemento.textContent = `$${(producto.precio * cantidad).toFixed(2)}`;
      ActualizarPrecios();
    }
  });

  // Actualizar totales
  function ActualizarPrecios(){
    const precios = document.querySelectorAll('.precio-unitario');
    const subtotal = document.getElementById('resumen-subtotal');
    const pagar = document.getElementById('modal-total');
    const total = document.getElementById('txtTotal');

    let subTotal = 0;
    precios.forEach(precio => {
      let valor = parseFloat(precio.textContent.replace('$','').trim());
      subTotal += valor;
    });

    subtotal.textContent = `$${subTotal.toFixed(2)}`;
    pagar.textContent = `$${subTotal.toFixed(2)}`;
    total.value = subTotal.toFixed(2);

    const ids = carrito.map(p => p.id).join(',');
    document.getElementById('txtIdProducto').value = ids;

    const cantidades = carrito.map((p,i) => {
      const card = document.querySelectorAll('.card')[i];
      return card.querySelector('.cantidad').textContent;
    }).join(',');
    document.getElementById('txtCantidad').value = cantidades;
  }

  ActualizarPrecios();

  // Modal de advertencia
  const mensaje = document.getElementById('alerta').querySelector('strong');
  const form = document.getElementById('formFinalizarCompra');
  const continuar = document.getElementById('btnContinuarAdvertencia');

  continuar.addEventListener('click', () => {
    // Si hay productos válidos, enviar
    if(idsEnviar && idsEnviar.length > 0){
      document.getElementById('txtIdProducto').value = idsEnviar.join(',');
      document.getElementById('txtCantidad').value = cantidadesEnviar.join(',');
      form.submit();
    } else {
      mensaje.textContent = `No hay ningún producto para realizar la compra`;
    }
  });

  // Envío del formulario
  form.addEventListener('submit', function(e){
    e.preventDefault();
    const cards = document.querySelectorAll('.card');

    let agotados = [];
    idsEnviar = [];
    cantidadesEnviar = [];

    carrito.forEach((p,i) => {
      const cantidad = parseInt(cards[i].querySelector('.cantidad').textContent);
      if(cantidad > parseInt(p.existencia)){
        agotados.push(p.nombre);
      } else {
        idsEnviar.push(p.id);
        cantidadesEnviar.push(cantidad);
      }
    });

    if(agotados.length > 0){
      const modal = new bootstrap.Modal(document.getElementById('modalAdvertencia'));
      modal.show();
      mensaje.textContent = `El Producto "${agotados.join(', ')}" está agotado`;
    } else if(idsEnviar.length > 0){
      form.submit();
    } else {
      mensaje.textContent = `No hay ningún producto para realizar la compra`;
      const modal = new bootstrap.Modal(document.getElementById('modalAdvertencia'));
      modal.show();
    }
  });
});
