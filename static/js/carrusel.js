function scrollCarousel(id, direction) {
    const container = document.getElementById(id);
    const card = container.querySelector('.card');
    if (!card) return;
    const scrollAmount = card.offsetWidth + 16; // ancho tarjeta + margen
    container.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
  }

 function equalizeHeights() {
  document.querySelectorAll(".carousel-container").forEach(container => {
    let maxHeight = 0;
    const cards = container.querySelectorAll(".card");

    // reset para recalcular
    cards.forEach(c => c.style.height = "auto");

    // calcular la más alta
    cards.forEach(c => {
      if (c.offsetHeight > maxHeight) {
        maxHeight = c.offsetHeight;
      }
    });

    // aplicar altura máxima a todas
    cards.forEach(c => c.style.height = maxHeight + "px");
  });
}

// correr en load y resize
window.addEventListener("load", equalizeHeights);
window.addEventListener("resize", equalizeHeights);
