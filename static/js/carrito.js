document.addEventListener("DOMContentLoaded", () => {
  // Botones "Agregar al Carrito"
  document.querySelectorAll(".btn-agregar").forEach(btn => {
    btn.addEventListener("click", () => {
      if (btn.classList.contains("agregado")) {
        btn.innerHTML = "Agregar al Carrito";
        btn.classList.remove("bi-cart-check", "agregado");
        btn.classList.add("bi-cart3");
        btn.style.backgroundColor = "#6C2DC7";
      } else {
        btn.innerHTML = "Agregado al Carrito";
        btn.classList.remove("bi-cart3");
        btn.classList.add("bi-cart-check", "agregado");
        btn.style.backgroundColor = "#28a745";
      }
    });
  });

  // Carruseles (si usas en otras secciones)
  document.querySelectorAll(".slider-wrapper").forEach(wrapper => {
    const slider = wrapper.querySelector(".slider");
    const leftArrow = wrapper.querySelector(".left-arrow");
    const rightArrow = wrapper.querySelector(".right-arrow");

    const scrollAmount = 320;

    if (leftArrow && rightArrow && slider) {
      leftArrow.addEventListener("click", () => {
        slider.scrollBy({ left: -scrollAmount, behavior: "smooth" });
      });
      rightArrow.addEventListener("click", () => {
        slider.scrollBy({ left: scrollAmount, behavior: "smooth" });
      });
    }
  });
});
