document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const tituloInput = document.getElementById('titulo');
    const comentarioInput = document.getElementById('comentario');
    const mensajeExito = document.getElementById('mensajeExito');
    const btnAceptar = document.getElementById('btnAceptarModal');
    const modalEl = document.getElementById('modalExito');
    const modal = new bootstrap.Modal(modalEl);

    // Validación del formulario
    form.addEventListener('submit', function (e) {
        let valid = true;

        limpiarErrores(tituloInput);
        limpiarErrores(comentarioInput);

        if (tituloInput.value.trim() === '') {
            mostrarError(tituloInput, 'El título es obligatorio.');
            valid = false;
        }

        if (comentarioInput.value.trim() === '') {
            mostrarError(comentarioInput, 'El comentario no puede estar vacío.');
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
        }
    });

    [tituloInput, comentarioInput].forEach(input => {
        input.addEventListener('input', () => {
            limpiarErrores(input);
        });
    });

    function mostrarError(input, mensaje) {
        input.classList.add('is-invalid');
        let feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.innerText = mensaje;
        input.parentNode.appendChild(feedback);
    }

    function limpiarErrores(input) {
        input.classList.remove('is-invalid');
        const existingFeedback = input.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
    }

    // Mostrar el modal si hay mensaje de éxito
    if (mensajeExito) {
        const mensaje = mensajeExito.getAttribute('data-mensaje');
        if (mensaje) {
            document.querySelector('#modalExito .modal-body').textContent = mensaje;
            modal.show();

            // Cerrar automáticamente después de 10 segundos y redirigir
            setTimeout(() => {
                modal.hide();
                const urlRedireccion = document.getElementById('urlComentario').getAttribute('data-url');
                window.location.href = urlRedireccion;
            }, 10000);
        }
    }

    // Comportamiento del botón "Aceptar"
    if (btnAceptar) {
        btnAceptar.addEventListener('click', function (e) {
            e.preventDefault(); // Evita comportamiento por defecto
            modal.hide();

            // Redirige después de la animación
            setTimeout(() => {
                const urlRedireccion = document.getElementById('urlComentario').getAttribute('data-url');
                window.location.href = urlRedireccion;

            }, 300);
        });
    }
});
