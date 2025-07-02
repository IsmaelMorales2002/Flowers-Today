from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    #modificar despues
    path('',lambda request: redirect('login')),
    #Vistas
    path('login/',Vista_Login,name='login'),
    path('crear_cuenta/',Vista_Crear_Cuenta,name='registro'),
    path('perfil/', Vista_Ver_Perfil, name='ver_perfil'),
    path('perfil/editar/', Vista_Editar_Perfil, name='editar_perfil'),
    path('recuperar-password/', Vista_Recuperar_Password, name='recuperar_password'),
    path('nueva-password/<token>/', Vista_Nueva_Password, name='nueva_password'),
    path('inicio-admin/',Vista_Inicio_Administrador,name='inicio_admin'),
    path('perfil-admin/',Vista_Ver_Perfil_Admin,name='ver_perfil_admin'),
    #Logico
    path('IniciarSesion/',Iniciar_Sesion,name='IniciarSesion'),
    path('CrearCuenta/',Crear_Cuenta_Cliente,name='CrearCuenta'),
    path('CerrarSesion/',Cerrar_Sesion,name='CerrarSesion'),
    path('EditarPerfil/',EditarPerfil,name='EditarPerfil'),
    #Endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)