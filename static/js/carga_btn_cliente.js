document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-crear-cuenta-cliente');
    var submitButton = document.getElementById('btn-cliente');
    
    form.addEventListener('submit', function(e) {
    submitButton.innerHTML = 'Cargando...';
    submitButton.disabled = true;
    });
});