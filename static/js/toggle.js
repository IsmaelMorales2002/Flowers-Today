document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    togglePassword.addEventListener('click', function () {
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';
        togglePassword.textContent = isPassword ? 'Ocultar' : 'Mostrar';
    });
});