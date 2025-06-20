from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

#Funcion Vista_Login, Muestra la vista Login.html
def Vista_Login(request):
    return render(request,'login.html')

#Funcion Vista_Crear_Cuenta, Muestra la vista registro.html
def Vista_Crear_Cuenta(request):
    return render(request,'registro.html')

"""
Funcion: Crear_Cuenta_Cliente
Descripcion: 
Crea un nuevo registro en la tabla usuario en la base de datos,
con un rol de tipo Cliente bandera tipo C.
"""
def Crear_Cuenta_Cliente(request):
    nombre = request.POST.get('txtNombreN','').strip()
    apellido = request.POST.get('txtApellidoN','').strip()
    telefono = request.POST.get('txtTelefonoN','').strip()
    correo = request.POST.get('txtCorreoN','').strip()
    password = request.POST.get('txtPasswordN','').strip()

    if not all([nombre,apellido,telefono,correo,password]):
        return JsonResponse({'Ok': False, 'mensaje':'Todos los campos son obligatorios'})