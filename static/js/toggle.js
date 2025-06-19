document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    confirmPasswordInput.type = type;
    this.textContent = type === 'password' ? 'Mostrar' : 'Ocultar';
});