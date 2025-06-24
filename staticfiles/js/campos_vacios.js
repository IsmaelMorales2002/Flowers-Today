
  document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los inputs con la clase "is-invalid"
    const campos = document.querySelectorAll(".form-control.is-invalid");

    // Para cada uno de esos campos, agrega un evento "input"
    campos.forEach((campo) => {
      campo.addEventListener("input", () => {
        // Remueve la clase "is-invalid" cuando el usuario empieza a escribir
        campo.classList.remove("is-invalid");

        // Oculta el mensaje de error asociado a ese campo
        const feedback = campo.closest('.input-group').querySelector('.invalid-feedback');
        if (feedback) {
          feedback.style.display = 'none';  // Oculta el mensaje de error
        }
      });
    });
  });

