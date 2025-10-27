from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from app.views import *
from app.cliente import *
from app.administrador import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',lambda request: redirect('vista_inicio_cliente')),
    #Vistas Cliente
    path('inicio/',Vista_Inicio_Cliente,name='vista_inicio_cliente'),
    path('login/',Vista_Login,name='vista_login'),
    path('registro/',Vista_Registro,name='vista_registro'),
    path('recuperacion/',Vista_Recuperar_Password,name='vista_recuperar_password'),
    path('perfil/',Vista_Ver_Perfil_Cliente,name='vista_perfil_cliente'),
    path('editar_perfil/',Vista_Editar_Perfil_Cliente,name='vista_editar_perfil_cliente'),
    path('comentario/', vista_comentario, name='vista_comentario'),
    path('comentario/guardar/', guardar_comentario, name='guardar_comentario'),
    path('actualizar_credencial/<uidb64>/<token>/',Vista_Actualizar_Clave,name='vista_credencial'),
    path('carrito/',vista_carrito,name='vista_carrito'),
    path('historial/',Vista_Historial_Compras,name='vista_historial_compras'),
    path('configuracion/',Vista_Configuracion,name='vista_configuracion'),
    path('arreglos/',Vista_Arreglos,name='vista_arreglos'),
    path('flores/',Vista_Flores,name='vista_flores'),
    path('servicio/',Vista_Solicitar_Servicio,name='vista_servicio'),
    path('solicitudes/',Vista_SolicitudesPedidos,name='vista_solicitudesPedidos'),

    #Vistas Administrador
    path('administracion/',Vista_Inicio_Administrador,name='vista_inicio_administrador'),
    path('perfil/administrador',Vista_Perfil_Admin,name='vista_perfil_administrador'),
    path('editar_perfil/administrador',Vista_Editar_Perfil_Admin,name='vista_editar_perfil_administrador'),
    path('clientes/',Vista_Clientes_Administracion,name='vista_clientes_administracion'),
    path('administradores/',Vista_Administradores_Administracion,name='vista_administradores_administracion'),
    path('crear_cuenta/',Vista_Crear_Cliente,name='vista_crear_cuenta'),
    path('crear_cuenta_admi/',Vista_Crear_Admi,name='vista_crear_cuenta_admi'),
    path('categoria/',Vista_Categoria_Administracion,name='vista_categoria_administracion'),
    path('crear_categoria/',Vista_Crear_Categoria,name='vista_crear_categoria'),
    path('editar-categoria/<int:id_categoria>/', Vista_Editar_Categoria, name='vista_editar_categoria'),
    path('editar-categoria-servicio/<int:id_categoria_servicio>/', Vista_Editar_Categoria_Servicio, name='vista_editar_categoriaServicio'),
    path('administradores/editar/vista/<int:id>/', Vista_Editar_Admi, name='vista_editar_admi'),
    path('clientes/editar/vista/<int:id>/',Vista_Editar_Cliente_Admin,name='vista_editar_cliente_admin'),
    path('productos/',Vista_Productos,name='vista_productos_administracion'),
    path('agregar-producto/',Vista_Agregar_Producto,name='vista_agregar_producto'),
    path('editar-producto/<int:id>',Vista_Actualizar_Producto,name='vista_actualizar_producto'),
    path('comentario/administracion/', vista_comentario_administracion, name='vista_comentario_administracion'),
    path('pedidos/administracion/', vista_pedidos_administracion, name='vista_pedidos_administracion'),
    path('categoria/servicios',Vista_Categoria_Servicio_Administracion,name='vista_categoria_servicio'),
    path('crear_categoria_servicio/',Vista_Crear_Categoria_Servicio,name='vista_crear_categoria_servicio'),
    path('gestion-solicitudes/',Vista_Solicitudes_Pedidos_Admin,name='vista_gestion_solicitudes'),

 
    #Logica
    path('CreaCuentaCliente',Crear_Cuenta_Cliente,name='CrearCuentaCliente'),
    path('IniciarSesion/',Iniciar_Sesion,name='IniciarSesion'),
    path('CerrarSesion/',Cerrar_Sesion,name='CerrarSesion'),
    path('EditarPerfilCliente/',Editar_Perfil_Cliente,name='EditarPerfilCliente'),
    path('EditarPerfilAdmin/',Editar_Perfil_Admin,name='EditarPerfilAdmin'),
    path('CreaCuentaAdmi',Crear_Cuenta_Admi,name='CrearCuentaAdmi'),
    path('CreaCategoria',Crear_Categoria,name='CrearCategoria'),
    path('CreaCategoriaServicio',Crear_Categoria_Servicio,name='CrearCategoriaServicio'),
    path('editar-categoria/guardar/<int:id_categoria>/', Editar_Categoria, name='editar_categoria'),
    path('editar-categoriaServicio/guardar/<int:id_categoria_servicio>/', Editar_CategoriaServicio, name='editar_categoriaServicio'),
    path('categoria/cambiar-estado/', cambiar_estado_categoria, name='cambiar_estado_categoria'),
    path('categoriaServicio/cambiar-estado/', cambiar_estado_categoria_servicio, name='cambiar_estado_categoriaServicio'),
    path('CorreoRecuperacion/',Correo_Recuperacion,name='CorreoRecuperacion'),
    path('administradores/editar/<int:id>/', Editar_Cuenta_Admi, name='EditarCuentaAdmi'),
    path('administradores/cambiar-estado/', cambiar_estado_administrador, name='cambiar_estado_administrador'),
    path('clientes/cambiar-estado/', cambiar_estado_Cliente, name='cambiar_estado_cliente'),
    path('ActualizarClave/<uidb64>/<token>/',Actualizar_Clave,name='ActualizarClave'),
    path('clientes/editar/<int:id>',Editar_Cuenta_Cliente,name='EditarCuentaCliente'),
    path('CrearProducto/',Crear_Producto,name='CrearProducto'),
    path('EditarProducto/<int:id>/',Editar_Producto,name='EditarProducto'),
    path('productos/cambiar-estado/',Cambiar_Estado_Producto,name='cambiar_estado_producto'),
    path('RealizarCompra/',RealizarCompra,name='RealizarCompra'),
    path('ActualizarClave/',ActualizarClaveCliente,name='ActualizarClaveCliente'),
    path('DesctivarCuenta/',DesactivarCuenta,name='DesactivarCuenta'),
    path('CrearServicio/',RegistrarServicio,name='CrearServicio'),
    path('CrearComentario/',CrearComentario,name='CrearComentario'),
    path('RepuestaCliente/',RespuestaCliente,name='RespuesCliente'),
    #Apis
    path('detalleCompra/<int:compra_id>',GET_Detalle_Compra,name='getdetalleCompras'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)