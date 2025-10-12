document.addEventListener('DOMContentLoaded', () =>{

    const actualizarIconoCarrito = () =>{
        let icono_carrito = document.getElementById('items-carrito')
        let carrito_data = JSON.parse(localStorage.getItem('carrito')) || []

        if(carrito_data.length > 0){
            icono_carrito.style.display = 'inline-block'
            icono_carrito.innerHTML = carrito_data.length
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
                console.log(carrito_data)
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

})