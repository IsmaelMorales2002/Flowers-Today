document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-crear-cuenta');
    var submitButton = document.getElementById('btn');
    
    form.addEventListener('submit', function(e) {
    submitButton.innerHTML = 'Cargando...';
    submitButton.disabled = true;
    });
});