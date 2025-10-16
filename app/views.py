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
#Generacion de Tokens
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import token_generator
from app.generar_comprobante import *

# Vista_Inicio, muestra la vista inicio.html
def Vista_Inicio_Cliente(request):
    # Solo productos activos
    productos = Producto.objects.filter(producto_activo=True)
    
    # Solo categorías activas que tienen productos activos relacionados
    categorias = Categoria.objects.filter(
        estado_categoria=True,
        producto__producto_activo=True  # relación inversa hacia productos
    ).distinct()
    
    activo = request.session.get('activo', False)
    
    return render(request, 'inicio.html', {
        'activo': activo,
        'productos': productos,
        'categorias': categorias
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

#Vista de actualizar clave
def Vista_Actualizar_Clave(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Usuario.objects.get(id_usuario=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario is not None and token_generator.check_token(usuario,token):
        return render(request,'nueva_password.html',{
            'uidb64': uidb64, 
            'token': token
        })
    else:
        return render(request,'token_invalido.html')
    
#Logica para actualizar contraseña
def Actualizar_Clave(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Usuario.objects.get(id_usuario=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None
        return redirect('vista_login')

    if usuario and token_generator.check_token(usuario,token):
        nueva_pass = request.POST.get('txtPasswordNueva').strip()
        usuario.password_usuario = make_password(nueva_pass)
        usuario.save()
        messages.success(request,"Contraseña Actualizada")
        return redirect('vista_login')

#Logica Para enviar correos de recuperacion de clave 
def Correo_Recuperacion(request):
    correo_destinatario = request.POST.get('txtCorreoUsuario').strip()
    contexto = {}

    if correo_destinatario:
        contexto['correo'] = correo_destinatario
        try: 
            usuario = Usuario.objects.get(correo_usuario=correo_destinatario)
        except Usuario.DoesNotExist:
            contexto['error_usuario'] = 'Usuario No Encontrado'
            return render(request,'recuperar_password.html',contexto)
        
        # Generar UID y Tokem
        uid = urlsafe_base64_encode(force_bytes(usuario.id_usuario))
        token = token_generator.make_token(usuario)

        # Enlace de recuperacion
        enlace_recuperacion = request.build_absolute_uri(
            reverse('vista_credencial',kwargs={'uidb64':uid, 'token': token})
        )

        # Renderizar Plantilla HTML
        mensaje = render_to_string('recuperacion.html',{
            'enlace_recuperacion': enlace_recuperacion
        })

        # Enviar Correo
        email = EmailMessage(
            'Recuperación de Contraseña',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [correo_destinatario]
        )
        email.content_subtype = 'html'
        email.send()
        messages.success(request,'!Enviado!')
        return redirect('vista_recuperar_password')
    
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

#Vista Editar Cliente desde Administracion
def Vista_Editar_Cliente_Admin(request,id):
    # Protección de ruta
    activo = request.session.get('activo_administrador', False)

    if activo:
        try:
            cliente = Usuario.objects.get(id_usuario = id)
            return render(request,'editarCliente.html',{
                'cliente': cliente,
                'activo': activo
            })
        except Usuario.DoesNotExist:
            return redirect('vista_clientes_administracion')
    return redirect('vista_inicio_cliente')


def vista_comentario_administracion(request):
    activo = request.session.get('activo_administrador', False)
    if activo:
        try:
            nombre = request.session.get('nombre_administrador', '')
            apellido = request.session.get('apellido_administrador', '')
            comentarios = Comentario.objects.select_related('id_usuario').order_by('-fecha_comentario')

            contexto = {
                'activo': activo,
                'nombre': nombre,
                'apellido': apellido,
                'comentarios': comentarios,
            }
            return render(request, 'comentarios_administracion.html', contexto)
        except KeyError:
            return redirect('vista_inicio_cliente')
    return redirect('vista_inicio_cliente')


# Vista_Productos
def Vista_Productos(request):
    # Protección de ruta
    activo = request.session.get('activo_administrador', False)
    if activo:
        productos = Producto.objects.all()
        return render(request,'productos_administracion.html',{
            'productos' : productos,
            'activo': activo
        })
    return redirect('vista_inicio_cliente')
    
# Vista_Agregar_Producto
def Vista_Agregar_Producto(request):
    # Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        categorias = Categoria.objects.all()
        return render(request,'agregar_producto.html',{
            'activo': activo,
            'categorias': categorias
        })
    return redirect('vista_inicio_cliente')

# Vista_Actualizar_Producto
def Vista_Actualizar_Producto(request,id):
    # Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        producto = Producto.objects.get(id_producto=id)
        categorias = Categoria.objects.all()
        return render(request,'editar_producto.html',{
            'activo': activo,
            'producto': producto,
            'categorias': categorias
        })
    return redirect('vista_inicio_cliente')



def vista_pedidos_administracion(request):
    activo = request.session.get('activo_administrador', False)
    if not activo:
        return redirect('vista_inicio_cliente')

    nombre = request.session.get('nombre_administrador', '')
    apellido = request.session.get('apellido_administrador', '')

    if request.method == 'POST' and 'cambiar_estado' in request.POST:
        cambiar_estado_pedido(request)
        return redirect('vista_pedidos_administracion')

    if request.GET.get('pdf'):
        return generar_comprobante_pdf(request.GET.get('pdf'))

    pedidos = listar_pedidos()

    return render(request, 'pedidos_administracion.html', {
        'activo': activo,
        'nombre': nombre,
        'apellido': apellido,
        'pedidos': pedidos,
    })

#Vista para visualizar el carrito
def vista_carrito(request):
    activo = request.session.get('activo',False)
    productos = Producto.objects.all()
    if activo:
        return render(request,'carrito.html',{
            'activo': activo,
            'productos': productos
        })
    return redirect('vista_inicio_cliente')

#Vista Ver_Perfil_Admin
def Vista_Perfil_Admin(request):
    #proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            admin = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
            return render(request,'perfilAdministrador.html',{
                'activo': activo,
                'usuario': admin
            })
        except Usuario.DoesNotExist:
            return redirect('vista_inicio_cliente')
    return redirect('vista_inicio_cliente')

#Vista Vista_Editar_Perfil_Admin    
def Vista_Editar_Perfil_Admin(request):
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            admin = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
            return render(request,'editar_perfilAdmin.html',{
                'activo': activo,
                'usuario': admin
            })
        except Usuario.DoesNotExist:
            return redirect('vista_inicio_cliente')
    return redirect('vista_inicio_cliente')
        
#Vista Vista_Historial_Compras
def Vista_Historial_Compras(request):
    activo = request.session.get('activo',False)
    if activo:
        try:
            usuario = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))
            compras = Compra.objects.filter(id_usuario = usuario.id_usuario)
            print(compras)
            return render(request,'historial_compras.html',{
                'activo': activo,
                'compras' : compras
            })    
        except Compra.DoesNotExist:
            return redirect('vista_inicio_cliente')
    return redirect('vista_inicio_cliente')
