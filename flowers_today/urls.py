from django.contrib import admin
from django.urls import path
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



    #Logico
    path('IniciarSesion/',Iniciar_Sesion,name='IniciarSesion'),
    path('CrearCuenta/',Crear_Cuenta_Cliente,name='CrearCuenta'),
    path('CerrarSesion/',Cerrar_Sesion,name='CerrarSesion')
    #Endpoints
]
