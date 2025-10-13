document.addEventListener('DOMContentLoaded', () =>{

    const actualizarIconoCarrito = () =>{
        let icono_carrito = document.getElementById('items-carrito')
        let carrito_data = JSON.parse(localStorage.getItem('carrito')) || []

        if(carrito_data.length > 0){
            icono_carrito.style.display = 'inline-block'
            icono_carrito.innerHTML = carrito_data.length
        }
        if(carrito_data.length == 0){
            icono_carrito.style.display = 'none'
        }
    }

    actualizarIconoCarrito();

    document.querySelectorAll('.btn-agregar').forEach(btn =>{
        btn.addEventListener('click', () =>{
            let carrito_data = JSON.parse(localStorage.getItem('carrito')) || []
            
            
            if(btn.classList.contains("agregado")){
                let id = btn.dataset.id
                carrito_data = carrito_data.filter(item => item.id !== id)
                localStorage.setItem('carrito',JSON.stringify(carrito_data))
                actualizarIconoCarrito();
            }else{
                let id = btn.dataset.id
                let nombre = btn.dataset.nombre
                let imagen = btn.dataset.imagen
                let precio = btn.dataset.precio
                let descripcion = btn.dataset.descripcion
    
                let producto = {id,nombre,imagen,precio,descripcion}
    
                carrito_data.push(producto)
                localStorage.setItem('carrito',JSON.stringify(carrito_data))
                actualizarIconoCarrito();
            }
        })
    })

    // Actulizacion Cuando se recarga la pagina
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const botones = document.querySelectorAll('.btn-agregar');

    if (carrito.length > 0) {
        carrito.forEach(producto => {
            const boton = document.querySelector(`.btn-agregar[data-id="${producto.id}"]`);
            if (boton) {
                boton.textContent = "Agregado al carrito";
                boton.classList.add("agregado", "bi-cart-check");
                boton.classList.remove("bi-cart3");
                boton.style.backgroundColor = "#28a745";
            }
        });
    }
})