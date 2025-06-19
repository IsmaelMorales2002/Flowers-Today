  const telefono = document.getElementById('telefono');
  
  telefono.addEventListener('input', function () {
    // Elimina todo lo que no sea número
    this.value = this.value.replace(/[^0-9]/g, '');
  });

  telefono.addEventListener('keypress', function (e) {
    // Previene la entrada de cualquier tecla que no sea un número
    if (!/[0-9]/.test(e.key)) {
      e.preventDefault();
    }
  });