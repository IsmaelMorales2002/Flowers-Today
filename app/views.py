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
    return render(request,'inicio.html',{
            'activo': activo
    })
    
def Vista_Inicio_Administrador(request):
    #Proteccion de Ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        return render(request,'inicioAdministrador.html',{
                'activo': activo
        })
    return redirect('vista_login')

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

    contexto = {}
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
        else:
            contexto['error_credenciales'] = 'Credenciales Incorrectas'
            contexto['correo'] = correo
            return render(request,'login.html',contexto)

    except Usuario.DoesNotExist:
        contexto['error_usuario'] = 'Usuario No Encontrado'
        return render(request,'login.html',contexto)
    
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
    
# Vista_Recuperar_Password, muestra la vista recuperar_password.html
def Vista_Recuperar_Password(request):
    return render(request,'recuperar_password.html')

# Vista_Ver_Perfil_Cliente, muestra la vista perfilCliente.html
def Vista_Ver_Perfil_Cliente(request):
    #Proteccion de ruta
    activo = request.session.get('activo',False)
    if activo:
        try:
            #Conocer informacion del cliente
            cliente = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
            return render(request,'perfilCliente.html',{
                'activo': activo,
                'usuario': cliente
            })
        except Usuario.DoesNotExist:
            return redirect('vista_login')
    else:
        return redirect('vista_login')
    
# Vista_Editar_Perfil_Cliente, muestra la vista editar_perfilCliente
def Vista_Editar_Perfil_Cliente(request):
    #Proteccion de ruta
    activo = request.session.get('activo',False)
    if activo:
        try:
            #Conocer informacion del cliente
            cliente = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
            return render(request,'editar_perfilCliente.html',{
                'activo': activo,
                'usuario': cliente
            })
        except Usuario.DoesNotExist:
            return redirect('vista_login')
    else:
        return redirect('vista_login')

# Vista_Clientes_Administracion, muestra la vista clientes_administracion
def Vista_Clientes_Administracion(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            usuarios = Usuario.objects.filter(id_rol__nombre_rol = 'C')
            return render(request,'clientes_administracion.html',{
                'activo' : activo,
                'usuarios': usuarios
            })
        except Exception:
            return redirect('vista_inicio_administrador')

    return redirect('vista_login')

# Vista_Crear_Cliente, muestra la vista crearCliente.html
def Vista_Crear_Cliente(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        return render(request,'crearCliente.html',{
            'activo':activo
        })
    return redirect('vista_login')

def Vista_Administradores_Administracion(request):
   #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            usuarios = Usuario.objects.filter(id_rol__nombre_rol = 'A')
            return render(request,'admi_administracion.html',{
                'activo' : activo,
                'usuarios': usuarios
            })
        except Exception:
            return redirect('vista_inicio_administrador')

    return redirect('vista_login')

def Vista_Crear_Admi(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        return render(request,'crearAdmi.html',{
            'activo':activo
        })
    return redirect('vista_login')
