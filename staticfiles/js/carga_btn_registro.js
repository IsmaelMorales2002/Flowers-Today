document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-crear-cuenta');
    var submitButton = document.getElementById('btn');
    
    form.addEventListener('submit', function(e) {
    // Cambiar el texto y deshabilitar el botón al hacer submit
    submitButton.innerHTML = 'Cargando...';  // Cambiar texto
    submitButton.disabled = true;  // Deshabilitar botón
    });
});