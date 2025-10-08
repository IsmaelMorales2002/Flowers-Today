document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.textContent = type === 'password' ? 'Mostrar' : 'Ocultar';
});

document.getElementById('togglePasswordConfirm').addEventListener('click', function () {
    const passwordInput = document.getElementById('password_confirm');
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.textContent = type === 'password' ? 'Mostrar' : 'Ocultar';
});

document.getElementById('form-nueva-password').addEventListener('submit', function (event) {
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('password_confirm').value.trim();
    const errorDiv = document.getElementById('error-password');
    const btnEnviarPass = document.getElementById('btnEnviarPass');
    errorDiv.textContent = '';

    btnEnviarPass.disabled = true;
    btnEnviarPass.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Enviando...';

    function reactivarBoton() {
        btnEnviarPass.disabled = false;
        btnEnviarPass.innerHTML = 'Guardar Contraseña';
    }

    if (!password || !confirmPassword) {
        event.preventDefault();
        errorDiv.textContent = 'La contraseña no puede estar vacía';
        reactivarBoton();
        return false;
    }

    if (password !== confirmPassword) {
        event.preventDefault();
        errorDiv.textContent = 'Las contraseñas no coinciden.';
        reactivarBoton();
        return false;
    }
});
