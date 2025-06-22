from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

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

    campos_vacios = []
    if not nombre:
        campos_vacios.append('nombre')
    if not apellido:
        campos_vacios.append('apellido')
    if not telefono:
        campos_vacios.append('telefono')
    if not correo:
        campos_vacios.append('correo')
    if not password_plano:
        campos_vacios.append('password')

    contexto = {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'correo': correo,
            'campos_vacios': campos_vacios
    }
    if campos_vacios:
        messages.warning(request,'Porfavor no dejar campos en blanco')
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
        request.session['usuario_apellido'] = cliente.apellido_usuario
        request.session['usuario_correo'] = cliente.correo_usuario
        request.session['usuario_correo'] = cliente.correo_usuario
        return redirect('inicio')
    except Exception as e:
        messages.error(request,'!Error!, Cuenta no creada')

    return redirect('login')

#Funcion Vista_Inicio, Muestra la vista Inicio.html
def Vista_Inicio(request):
    correo = request.session.get('usuario_correo',None)
    return render(request,'inicio.html',{
        'correo': correo
    })

"""Funcion: Iniciar_Sesion
Descripcion:
Verifica que el correo y contraseña sean los correcto para darle acceso al sistema
"""
def Iniciar_Sesion(request):
    correo = request.POST.get('txtCorreo')
    password = request.POST.get('txtPassword')

    try:
        usuario = Usuario.objects.get(correo_usuario = correo)
        
        #Verificacion de contraseña
        if check_password(password,usuario.password_usuario):
            #Session para guardar informacion del cliente
            request.session['usuario_nombre'] = usuario.nombre_usuario
            request.session['usuario_apellido'] = usuario.apellido_usuario
            request.session['usuario_correo'] = usuario.correo_usuario
            return redirect('inicio')
        else:
            messages.warning(request,'Credenciales Incorrectas')
            return render(request,'login.html',{
                'activo': request.session.get('usuario_correo')
            })

    except Usuario.DoesNotExist:
        messages.error(request,'!Usuario No Encontrado!')
        return redirect('login')



#Funcion Cerrar_Sesion, Cierra Session y elimina las session creadas
def Cerrar_Sesion(request):
    del request.session['usuario_correo']
    del request.session['usuario_apellido']
    del request.session['usuario_nombre']
    return redirect('login')

#Funcion Vista_Ver_Perfil, Muestra la vista perfil.html
# Esta vista puede ser utilizada para mostrar la informacion del usuario logueado
def Vista_Ver_Perfil(request):
    return render(request, 'perfil.html',{
        'activo': request.session.get('usuario_correo')
    })

#Funcion Vista_Editar_Perfil, Muestra la vista editar_perfil.html
# Esta vista puede ser utilizada para editar la informacion del usuario logueado
def Vista_Editar_Perfil(request):
    return render(request, 'editar_perfil.html')

#Funcion Vista_Recuperar_Password, Muestra la vista recuperar_password.html
# Esta vista puede ser utilizada para iniciar el proceso de recuperacion de contraseña
def Vista_Recuperar_Password(request):
    return render(request, 'recuperar_password.html')

def Vista_Nueva_Password(request, token):
    return render(request, 'nueva_password.html', {'token': token})

