document.addEventListener("DOMContentLoaded", function () {
  const campos = document.querySelectorAll(".form-control.is-invalid");

  campos.forEach((campo) => {
    campo.addEventListener("input", () => {
      campo.classList.remove("is-invalid");
      const feedback = campo.closest('.input-group').querySelector('.invalid-feedback');
      if (feedback) {
        feedback.style.display = 'none';
      }
    });
  });
});

