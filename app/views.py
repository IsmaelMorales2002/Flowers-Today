from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q

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
        messages.error(request,'Dejo Un Campo Vacio, Cuenta No Creada')

    #Validacion para crear registro en Tabla Usuario
    try:
        #Validacion para crear registro en Tabla ROL
        # try: 
        #     #Creacion de Registro Rol
        #     rol = Rol(
        #         nombre_rol = 'C'
        #     )
        #     rol.save()
        # except Exception:
        #     messages.error(request,'Error Al Crear La Cuenta')
        #     return redirect('registro')
            #Terminar Validacion ROL

        #Validacion De Correo Y Telefono
        try:
            datosExistentes = Usuario.objects.filter(
                Q(correo_usuario = correo) | Q(telefono_usuario = telefono)).first()
            if datosExistentes:
                messages.warning(request,'Correo o Telefono Ya Registrado')
                contexto = {
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'correo': correo,
                }
                return render(request,'registro.html',contexto)
            
            #Creacion de Registro Usuario
            usuario = Usuario(
                # id_rol = rol,
                nombre_usuario = nombre,
                apellido_usuario = apellido,
                telefono_usuario = telefono,
                correo_usuario = correo,
                password_usuario = password,
                usuario_activo = True
            )
            print('PASO LA PRUEBA')
            # usuario.save()
            return redirect('login')
        except Exception as e:
            return redirect('registro')
    except Exception as e:
        messages.error(request,'Actualmente No Se Puede Registrar Su Cuenta')
        return  render(request,'login.html')