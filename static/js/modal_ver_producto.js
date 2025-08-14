document.addEventListener('DOMContentLoaded', function () {
  const modalCategoria = document.getElementById('modal-categoria');
  const modalNombreProducto = document.getElementById('modal-nombre-producto');
  const modalDescripcion = document.getElementById('modal-descripcion');
  const modalCantidadMaxima = document.getElementById('modal-cantidad-maxima');
  const modalCantidadMinima = document.getElementById('modal-cantidad-minima');
  const modalPrecio = document.getElementById('modal-precio');
  const modalTipoProducto = document.getElementById('modal-tipo-producto');
  const modalEstadoProducto = document.getElementById('modal-estado-producto');
  const modalImagenProducto = document.getElementById('modal-imagen-producto');

  // Delegación de eventos (compatible con DataTables Responsive)
  $(document).on('click', '.btn-ver-producto', function () {
    const $btn = $(this);

    const categoria = $btn.data('categoria');
    const nombre = $btn.data('nombre');
    const descripcion = $btn.data('descripcion');
    const cantidadMaxima = $btn.data('cantidad-maxima');
    const cantidadMinima = $btn.data('cantidad-minima');
    const precio = $btn.data('precio');
    const tipo = $btn.data('tipo');
    const estado = $btn.data('estado') === true || $btn.data('estado') === 'True';
    const imagen = $btn.data('imagen') && $btn.data('imagen').trim() !== ''
      ? $btn.data('imagen')
      : "{% static 'img/producto-default.png' %}";

    // Asignar valores en el modal
    modalCategoria.textContent = categoria;
    modalNombreProducto.textContent = nombre;
    modalDescripcion.textContent = descripcion;
    modalCantidadMaxima.textContent = cantidadMaxima;
    modalCantidadMinima.textContent = cantidadMinima;
    modalPrecio.textContent = parseFloat(precio).toFixed(2);
    modalTipoProducto.textContent = tipo;
    modalEstadoProducto.textContent = estado ? 'Activo' : 'Inactivo';
    modalImagenProducto.src = imagen;

    // Colorear estado
    modalEstadoProducto.classList.remove('text-success', 'text-danger');
    modalEstadoProducto.classList.add(estado ? 'text-success' : 'text-danger');
  });
});
