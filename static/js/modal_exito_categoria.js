document.addEventListener('DOMContentLoaded', function () {
  // Busca los mensajes ocultos que indiquen éxito en creación o edición
  const messages = JSON.parse(document.getElementById('mensajes-json')?.textContent || '[]');

  messages.forEach(message => {
    if (message.tags === 'success') {
      if (message.message.includes('Categoría creada exitosamente')) {
        const modalCreado = new bootstrap.Modal(document.getElementById('modalCreadoExitoCategoria'));
        modalCreado.show();
      }
      else if (message.message === 'categoria_editada') {
        const modalEditado = new bootstrap.Modal(document.getElementById('modalEditadoExitoCategoria'));
        modalEditado.show();
      }
    }
  });
});
