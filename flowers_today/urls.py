from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from app.views import *
from app.cliente import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',lambda request: redirect('vista_login')),
    #Vistas
    path('inicio/',Vista_Inicio_Cliente,name='vista_inicio_cliente'),
    path('login/',Vista_Login,name='vista_login'),
    path('registro/',Vista_Registro,name='vista_registro'),
    #Logica
    path('CreaCuentaCliente',Crear_Cuenta_Cliente,name='CrearCuentaCliente')
    #Endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)