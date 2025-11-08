document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-iniciar-sesion');
    var submitButton = document.getElementById('btn-login');
    
    form.addEventListener('submit', function(e) {
    // Cambiar el texto y deshabilitar el botón al hacer submit
    submitButton.innerHTML = 'Cargando...';  // Cambiar texto
    submitButton.disabled = true;  // Deshabilitar botón
    });
});