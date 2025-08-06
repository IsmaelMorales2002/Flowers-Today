document.addEventListener('DOMContentLoaded', function () {
        const from = document.getElementById('form-recuperar-password')
        const btnEnviar = document.getElementById('btnEnviar')

        from.addEventListener('submit', () =>{
            btnEnviar.disabled = true;
            btnEnviar.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Enviando...';
        })

        let modalPassword = new bootstrap.Modal(document.getElementById('modalEnviadoExito'));
        modalPassword.show();
});