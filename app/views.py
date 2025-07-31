from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render,redirect
from app.administrador import *
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
    return redirect('vista_inicio_cliente')

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
            return redirect('vista_inicio_cliente')
    else:
        return redirect('vista_inicio_cliente')
    
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
            return redirect('vista_inicio_cliente')
    else:
        return redirect('vista_inicio_cliente')

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

    return redirect('vista_inicio_cliente')

# Vista_Crear_Cliente, muestra la vista crearCliente.html
def Vista_Crear_Cliente(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        return render(request,'crearCliente.html',{
            'activo':activo
        })
    return redirect('vista_inicio_cliente')

def Vista_Administradores_Administracion(request):
   #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)

    if activo:
        try:
            id_actual = request.session.get('id_usuario')  # ID del usuario logueado
            usuarios = Usuario.objects.filter(id_rol__nombre_rol='A').exclude(id_usuario=id_actual)

            return render(request,'admi_administracion.html',{
                'activo' : activo,
                'usuarios': usuarios
            })
        except Exception:
            return redirect('vista_inicio_administrador')

    return redirect('vista_inicio_cliente')

def Vista_Crear_Admi(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        return render(request,'crearAdmi.html',{
            'activo':activo
        })
    return redirect('vista_inicio_cliente')


def Vista_Categoria_Administracion(request):
     #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            usuarios = Usuario.objects.filter(id_rol__nombre_rol = 'A')
            categorias = Categoria.objects.all()
            return render(request,'categoria_administracion.html',{
                'activo' : activo,
                'usuarios': usuarios,
                'categorias': categorias
            })
        except Exception:
            return redirect('vista_inicio_administrador')

    return redirect('vista_inicio_cliente')

def Vista_Crear_Categoria(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    
    if activo:
        return render(request,'crearCategoria.html',{
            'activo':activo
        })
    return redirect('vista_inicio_cliente')

def Vista_Editar_Categoria(request, id_categoria):
    activo = request.session.get('activo_administrador', False)
    if activo:
        try:
            categoria = Categoria.objects.get(id_categoria=id_categoria)
            contexto = {
                'activo': activo,
                'nombre': categoria.nombre_categoria,
                'id_categoria': id_categoria
            }
            return render(request, 'editar_categoria.html', contexto)
        except Categoria.DoesNotExist:
            return redirect('vista_categoria_administracion')

    return redirect('vista_login')

def vista_comentario(request):
    activo = request.session.get('activo', False)
    if activo:
        try:
            nombre = request.session.get('nombre_cliente', '')
            apellido = request.session.get('apellido_cliente', '')
            comentarios = Comentario.objects.select_related('id_usuario').order_by('-fecha_comentario')[:9]  # solo los 10 más recientes

            contexto = {
                'activo': activo,
                'nombre': nombre,
                'apellido': apellido,
                'comentarios': comentarios,
            }
            return render(request, 'comentario_formulario.html', contexto)
        except KeyError:
            return redirect('vista_login')
    return redirect('vista_login')

    return redirect('vista_inicio_cliente')

#Vista de actualizar clave
def Vista_Actualizar_Clave(request):
    return render(request,'nueva_password.html')

#Logica Para enviar correos de recuperacion de clave 
def Correo_Recuperacion(request):
    correo_destinatario = request.POST.get('txtCorreoUsuario')
    contexto = {}
    if correo_destinatario:
        contexto['correo'] = correo_destinatario
        existe = Usuario.objects.filter(correo_usuario=correo_destinatario).exists()
        if existe:
            asunto = 'Recuperación de Contraseña'
            enlace_recuperacion = request.build_absolute_uri(reverse('vista_credencial'))
            mensaje = render_to_string('recuperacion.html',{'enlace_recuperacion':enlace_recuperacion})
            correo_remitente = settings.DEFAULT_FROM_EMAIL
            email = EmailMessage(
                asunto,
                mensaje,
                correo_remitente,
                [correo_destinatario],
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request,'!Enviado!')
            return redirect('vista_recuperar_password')
        else:
            contexto['error_usuario'] = 'Usuario No Encontrado'
            return render(request,'recuperar_password.html',contexto)

def Vista_Editar_Admi(request, id):
    # Protección de ruta
    activo = request.session.get('activo_administrador', False)

    if activo:
        try:
            administrador = Usuario.objects.get(id_usuario=id)
            return render(request, 'editarAdmi.html', {
                'administrador': administrador,
                'activo': activo
            })
        except Usuario.DoesNotExist:
            return redirect('vista_administradores_administracion')  # si no existe, vuelve al listado
    return redirect('vista_inicio_cliente')


