from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #modificar despues
    path('',lambda request: redirect('inicio')),
    #Vistas
    path('login/',Vista_Login,name='login'),
    path('crear_cuenta/',Vista_Crear_Cuenta,name='registro'),
    path('inicio/',Vista_Inicio,name='inicio'),
    path('perfil/', Vista_Ver_Perfil, name='ver_perfil'),
    path('perfil/editar/', Vista_Editar_Perfil, name='editar_perfil'),
    path('recuperar-password/', Vista_Recuperar_Password, name='recuperar_password'),
    path('nueva-password/<token>/', Vista_Nueva_Password, name='nueva_password'),
    path('categoria/listar/', Vista_Listar_Categoria, name='listar_categoria'),
    path('categoria/insertar/', Vista_Insertar_Categoria, name='insertar_categoria'),
    path('producto/insertar/', Vista_Insertar_Producto, name='insertar_producto'),
    path('producto/listar/', Vista_Listar_Producto, name='listar_producto'),
    path('editar_producto/', Vista_Editar_Producto, name='editar_producto'),
    path('producto/cambiar_estado/', Vista_Cambiar_Estado_Producto, name='cambiar_estado_producto'),
    path('categoria/cambiar_estado/', cambiar_estado_categoria, name='cambiar_estado_categoria'),
    path('inicio-admin/',Vista_Inicio_Administrador,name='inicio_admin'),
    path('perfil-admin/',Vista_Ver_Perfil_Admin,name='ver_perfil_admin'),
    path('usuario/listar/', Vista_Listar_Usuarios, name='listar_usuarios'),
    path('categoria/actualizar/<int:id>',Vista_Actualizar_Categoria,name='actualizar_categoria'),


    #Logico
    path('IniciarSesion/',Iniciar_Sesion,name='IniciarSesion'),
    path('CrearCuenta/',Crear_Cuenta_Cliente,name='CrearCuenta'),
    path('CerrarSesion/',Cerrar_Sesion,name='CerrarSesion'),
    path('EditarPerfil/',EditarPerfil,name='EditarPerfil'),
    path('ActualizarCategoria',Actualizar_Categoria,name='ActualizarCategoria'),

    #Endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)