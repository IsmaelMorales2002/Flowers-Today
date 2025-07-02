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
        messages.warning(request,'Por favor No Dejar Campos En Blanco')
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
        request.session['usuario_nombre'] = cliente.nombre_usuario
        request.session['usuario_apellido'] = cliente.apellido_usuario
        request.session['usuario_correo'] = cliente.correo_usuario
        request.session['usuario_id'] = cliente.id_usuario
        return redirect('inicio')
    except Exception as e:
        messages.error(request,'!Error!, Cuenta no creada')

    return redirect('login')


#Funcion Vista_Inicio_Administrador, Muestra la vista InicioAdministrador.html
def Vista_Inicio_Administrador(request):
    activo_admin = request.session.get('admin_correo',None)
    if activo_admin:
        return render(request,'inicioAdministrador.html',{
            'activo_admin': activo_admin
        })
    return render(request,'inicio.html')

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
            if usuario.id_rol.nombre_rol == 'C':
                request.session['usuario_nombre'] = usuario.nombre_usuario
                request.session['usuario_apellido'] = usuario.apellido_usuario
                request.session['usuario_correo'] = usuario.correo_usuario
                request.session['usuario_id'] = usuario.id_usuario
                return redirect('inicio')
            
            elif usuario.id_rol.nombre_rol == 'A':
                request.session['admin_nombre'] = usuario.nombre_usuario
                request.session['admin_apellido'] = usuario.apellido_usuario
                request.session['admin_correo'] = usuario.correo_usuario
                request.session['admin_id'] = usuario.id_usuario
                return redirect('inicio_admin')
            
            else:
                messages.error(request,'!Usuario No Encontrado!')
                return redirect('login')
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
    try:
        usuario = Usuario.objects.get(id_usuario = request.session.get('usuario_id',None))
        if usuario.id_rol.nombre_rol == 'C':
            del request.session['usuario_correo']
            del request.session['usuario_apellido']
            del request.session['usuario_nombre']
            del request.session['usuario_id']
            return redirect('inicio')
    
    except Usuario.DoesNotExist as e:
        try:
            admin = Usuario.objects.get(id_usuario = request.session.get('admin_id',None))
            if admin.id_rol.nombre_rol == 'A': 
                del request.session['admin_correo']
                del request.session['admin_apellido']
                del request.session['admin_nombre']
                del request.session['admin_id']
                return redirect('inicio')
        except Usuario.DoesNotExist:
            return redirect('login')

#Funcion Vista_Ver_Perfil, Muestra la vista perfil.html
# Esta vista puede ser utilizada para mostrar la informacion del usuario logueado
def Vista_Ver_Perfil(request):
    #Seguridad de Rutas
    activo = request.session.get('usuario_correo',None)
    if activo:
        try:
            usuario = Usuario.objects.get(correo_usuario = activo)
            return render(request, 'perfil.html',{
                'activo': activo,
                'usuario': usuario
            })
        except Usuario.DoesNotExist:
            return redirect('inicio')
    else:
        return redirect('login')
    
def Vista_Ver_Perfil_Admin(request):
    #Seguridad de Rutas
    activo_admin = request.session.get('admin_correo',None)
    if activo_admin:
        try:
            usuario = Usuario.objects.get(correo_usuario = activo_admin)
            return render(request, 'perfilAdministrador.html',{
                'activo_admin': activo_admin,
                'usuario': usuario
            })
        except Usuario.DoesNotExist:
            return redirect('inicio')
    else:
        return redirect('login')


#Funcion Vista_Editar_Perfil, Muestra la vista editar_perfil.html
# Esta vista puede ser utilizada para editar la informacion del usuario logueado
def Vista_Editar_Perfil(request):
    activo = request.session.get('usuario_correo',None)
    if activo:
        try:
            usuario = Usuario.objects.get(correo_usuario = activo)
            return render(request,'editar_perfil.html',{
                'activo': activo,
                'usuario': usuario
            })
        except Usuario.DoesNotExist:
            return redirect('inicio')
    else:
        return redirect('login')

#Funcion Vista_Recuperar_Password, Muestra la vista recuperar_password.html
# Esta vista puede ser utilizada para iniciar el proceso de recuperacion de contraseña
def Vista_Recuperar_Password(request):
    return render(request, 'recuperar_password.html')

def Vista_Nueva_Password(request, token):
    return render(request, 'nueva_password.html', {'token': token})


""" Funcion: EditarPerfil
Descripcion:
Actualiza la informacion del cliente en la tabla Usuario
"""
def EditarPerfil(request):
    nombre = request.POST.get('txtNombreA','').strip()
    apellido = request.POST.get('txtApellidoA','').strip()
    telefono = request.POST.get('txtTelefonoA','').strip()
    correo = request.POST.get('txtCorreoA','').strip()
    imagen = request.FILES.get('imagen_usuario')

    campos_vacios = []
    if not nombre:
        campos_vacios.append('nombre')
    if not apellido:
        campos_vacios.append('apellido')
    if not telefono:
        campos_vacios.append('telefono')
    if not correo:
        campos_vacios.append('correo')

    if campos_vacios:
        messages.warning(request,'Por Favor No Dejar Campos En Blanco')
        return redirect('editar_perfil')
    
    #Verificacion de Actualziacion De Campos
    try:
        usuario = Usuario.objects.get(id_usuario = request.session.get('usuario_id',None))
        usuario.nombre_usuario = nombre
        usuario.apellido_usuario = apellido
        usuario.telefono_usuario = telefono
        usuario.correo_usuario = correo
        if imagen:
            usuario.imagen_usuario = imagen
        usuario.save()
        request.session['usuario_nombre'] = usuario.nombre_usuario
        request.session['usuario_apellido'] = usuario.apellido_usuario
        request.session['usuario_correo'] = usuario.correo_usuario
        return redirect('ver_perfil')
    except Usuario.DoesNotExist:
        messages.error(request,'!Error!, Actualización No Realizada')
        return redirect('editar_perfil')