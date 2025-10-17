document.addEventListener('click', (e) => {
    const comprobante = document.getElementById('comprobante')
    if(e.target.classList.contains('btn-ver-detalle')){
        e.preventDefault();

        const url = e.target.getAttribute('href');
        fetch(url)
            .then(res => res.json())
            .then(data => {
                const modal = document.getElementById("modalDetalleCompra");
                const tbody = modal.querySelector("tbody");
                const totalCell = modal.querySelector("#detalle-total");
                const modalTitulo = modal.querySelector(".modal-title");

                modalTitulo.textContent = `Detalle De Compra ${comprobante.textContent} `;
                tbody.innerHTML = "";

                data.productos.forEach(p => {
                    const fila = document.createElement("tr");
                    fila.innerHTML = `
                        <td><img src="${p.imagen}" width="60" class="rounded"></td>
                        <td>${p.nombre}</td>
                        <td>${p.cantidad}</td>
                        <td>$${parseFloat(p.precio).toFixed(2)}</td>
                        <td>$${parseFloat(p.subtotal).toFixed(2)}</td>
                    `;
                    tbody.appendChild(fila);
                });

                totalCell.textContent = `$${parseFloat(data.total).toFixed(2)}`;
            })
            .catch(err => console.error("Error al cargar detalle:", err));
    }
});
