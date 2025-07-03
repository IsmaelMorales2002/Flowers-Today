from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

# Vista_Inicio, muestra la vista inicio.html
def Vista_Inicio_Cliente(request):
    #Proteccion de Ruta
    activo = request.session.get('activo',False)
    if activo:
        return render(request,'inicio.html',{
            'activo': activo
        })
    else:
        return render(request,'inicio.html',{
            'activo': activo
        })

# Vista_Login, muestra la vista login.html
def Vista_Login(request):
    return render(request,'login.html')

# Vista_Registro, muestra la vista registro.html
def Vista_Registro(request):
    return render(request,'registro.html')

# Iniciar_Sesion, Logica para iniciar sesion
def Iniciar_Sesion(request):
    correo = request.POST.get('txtCorreo','').strip()
    password = request.POST.get('txtPassword','').strip()

    try: 
        usuario = Usuario.objects.get(correo_usuario = correo)

        #Verificacion de contraseña
        if check_password(password,usuario.password_usuario):
            #Session para guardar informacion del cliente
            if usuario.id_rol.nombre_rol == 'C':
                request.session['nombre_cliente'] = usuario.nombre_usuario
                request.session['apellido_cliente'] = usuario.apellido_usuario
                request.session['correo_cliente'] = usuario.correo_usuario
                request.session['id_usuario'] = usuario.id_usuario
                request.session['activo'] = True
                return redirect('vista_inicio_cliente')
            
            #Session paran guardar informacion del administrador
            elif usuario.id_rol.nombre_rol == 'A':
                request.session['nombre_administrador'] = usuario.nombre_usuario
                request.session['apellido_administrador'] = usuario.apellido_usuario
                request.session['correo_administrador'] = usuario.correo_usuario
                request.session['id_usuario'] = usuario.id_usuario
                request.session['activo_administrador'] = True
                return redirect('vista_inicio_administrador')
    
    except Usuario.DoesNotExist:
        messages.error(request,'!Usuario No Encontrado!')
        return redirect('vista_login')
    
# Cerrar_Sesion, logica para cerrar sesion
def Cerrar_Sesion(request):
    # Identificar que rol tiene para eliminar las request.sessiones corecctas
    try:
        cliente = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
        if cliente.id_rol.nombre_rol == 'C':
            del request.session['nombre_cliente']
            del request.session['apellido_cliente']
            del request.session['correo_cliente']
            del request.session['id_usuario']
            del request.session['activo']
            return redirect('vista_inicio_cliente')
        elif cliente.id_rol.nombre_rol == 'A':
            del request.session['nombre_administrador']
            del request.session['apellido_administrador']
            del request.session['correo_administrador']
            del request.session['id_usuario']
            del request.session['activo_administrador']
            return redirect('vista_inicio_cliente')
    except Usuario.DoesNotExist:
        return redirect('vista_login')