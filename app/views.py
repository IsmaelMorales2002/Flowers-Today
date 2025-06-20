from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

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
    password_plano = request.POST.get('txtPasswordN','').strip()

    contexto = {
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'correo': correo,
    }

    if not all([nombre,apellido,telefono,correo,password_plano]):
        messages.warning(request,'Porfavor No Dejar Campos En Blanco')
        return render(request,'registro.html',contexto)
    
    #Creacion de registro en tabla Rol en Base De Datos
    try:
        rol = Rol(
            nombre_rol = 'C'
        )
    #Termina la creacion del registro Rol

    #Verificacion de correo y telefono existente
        datosExistentes = Usuario.objects.filter(Q(correo_usuario = correo) | Q(telefono_usuario = telefono))
        if datosExistentes:
            messages.warning(request,'!Correo o Telefono, ya registrado!')
            return render(request,'registro.html',contexto)

        #Cifrar Contraseña
        password = make_password(password_plano)

    #Creacion de registo en tabla Usuario en Base De Datos
        cliente = Usuario(
            id_rol = rol,
            nombre_usuario = nombre,
            apellido_usuario = apellido,
            correo_usuario = correo,
            password_usuario = password,
            telefono_usuario = telefono,
            usuario_activo = True
        )
    #Termina la creacion del registro Usuario
    #Si todo salio bien , vamos a guardar todo en base de datos
        rol.save()
        cliente.save()
        messages.success(request,'!Cuenta Creada Con Exito!')

    except Exception:
        messages.error(request,'!Error!, Cuenta no creada')

    return redirect('login')