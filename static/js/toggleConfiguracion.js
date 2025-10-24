document.getElementById('toggleContraseñaActual').addEventListener('click', function() {
    const input = document.getElementById('contraseñaActual');
    if (input.type === "password") {
        input.type = "text";
        this.textContent = "Ocultar";
    } else {
        input.type = "password";
        this.textContent = "Mostrar";
    }
});

document.getElementById('toggleContraseñaNueva').addEventListener('click', function() {
    const input = document.getElementById('contraseñaNueva');
    if (input.type === "password") {
        input.type = "text";
        this.textContent = "Ocultar";
    } else {
        input.type = "password";
        this.textContent = "Mostrar";
    }
});

