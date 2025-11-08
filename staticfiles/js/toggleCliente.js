document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePasswordCliente');
    const passwordInput = document.getElementById('passwordCliente');

    togglePassword.addEventListener('click', function () {
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';
        togglePassword.textContent = isPassword ? 'Ocultar' : 'Mostrar';
    });
});