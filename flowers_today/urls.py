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
    path('actualizar_credencial/',Vista_Actualizar_Clave,name='vista_credencial'),
    #Vistas Administrador
    path('administracion/',Vista_Inicio_Administrador,name='vista_inicio_administrador'),
    path('clientes/',Vista_Clientes_Administracion,name='vista_clientes_administracion'),
    path('administradores/',Vista_Administradores_Administracion,name='vista_administradores_administracion'),
    path('crear_cuenta/',Vista_Crear_Cliente,name='vista_crear_cuenta'),
    path('crear_cuenta_admi/',Vista_Crear_Admi,name='vista_crear_cuenta_admi'),
    path('categoria/',Vista_Categoria_Administracion,name='vista_categoria_administracion'),
    path('crear_categoria/',Vista_Crear_Categoria,name='vista_crear_categoria'),
    path('editar-categoria/<int:id_categoria>/', Vista_Editar_Categoria, name='vista_editar_categoria'),


 
    #Logica
    path('CreaCuentaCliente',Crear_Cuenta_Cliente,name='CrearCuentaCliente'),
    path('IniciarSesion/',Iniciar_Sesion,name='IniciarSesion'),
    path('CerrarSesion/',Cerrar_Sesion,name='CerrarSesion'),
    path('EditarPerfilCliente/',Editar_Perfil_Cliente,name='EditarPerfilCliente'),
    path('CreaCuentaAdmi',Crear_Cuenta_Admi,name='CrearCuentaAdmi'),
    path('CreaCategoria',Crear_Categoria,name='CrearCategoria'),
    path('editar-categoria/guardar/<int:id_categoria>/', Editar_Categoria, name='editar_categoria'),
    path('categoria/cambiar-estado/', cambiar_estado_categoria, name='cambiar_estado_categoria'),
    path('CorreoRecuperacion/',Correo_Recuperacion,name='CorreoRecuperacion'),



    #Endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)