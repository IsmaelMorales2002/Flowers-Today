const modalEditar = document.getElementById('modalEditarCategoria');

modalEditar.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget; // Botón que activó el modal
    const id = button.getAttribute('data-id');
    const nombre = button.getAttribute('data-nombre');

    // Asignar valores a los campos del modal
    document.getElementById('editIdCategoria').value = id;
    document.getElementById('editNombreCategoria').value = nombre;
});
