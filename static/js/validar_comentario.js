document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const tituloInput = document.getElementById('titulo');
    const comentarioInput = document.getElementById('comentario');

    form.addEventListener('submit', function (e) {
        let valid = true;

        // Limpiar clases anteriores
        tituloInput.classList.remove('is-invalid');
        comentarioInput.classList.remove('is-invalid');

        // Eliminar alerta previa si existe
        const prevAlert = document.getElementById('alertCampos');
        if (prevAlert) {
            prevAlert.remove();
        }

        // Validaciones
        if (tituloInput.value.trim() === '') {
            tituloInput.classList.add('is-invalid');
            valid = false;
        }

        if (comentarioInput.value.trim() === '') {
            comentarioInput.classList.add('is-invalid');
            valid = false;
        }

        if (!valid) {
            e.preventDefault();

            // Crear alerta
            const alert = document.createElement('div');
            alert.id = 'alertCampos';
            alert.className = 'alert alert-danger alert-dismissible fade show mt-3';
            alert.role = 'alert';
            alert.innerHTML = `
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                Por favor completa todos los campos antes de enviar.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            // Insertar alerta antes del formulario
            form.parentElement.insertBefore(alert, form);

            // 🔁 Autocierre en 4 segundos
            setTimeout(() => {
                alert.classList.remove('show');
                alert.classList.add('fade');
                setTimeout(() => {
                    if (alert) alert.remove();
                }, 500); // espera a que termine la animación
            }, 4000);
        }
    });

    // Elimina el rojo al escribir
    [tituloInput, comentarioInput].forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('is-invalid');
        });
    });
});
