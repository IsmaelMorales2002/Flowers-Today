document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-recuperar-password');
    const btnEnviar = document.getElementById('btnEnviar');

    form.addEventListener('submit', function () {
        btnEnviar.disabled = true;
        btnEnviar.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Enviando...';
    });
});
