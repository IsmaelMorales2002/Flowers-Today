from datetime import datetime, timedelta, timezone as dt_timezone
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
import uuid
from django.db import transaction
from django.db.models import F

# Crear_Cuenta_Cliente, logica para crear cuenta tipo cliente
def Crear_Cuenta_Cliente(request):
    nombre = request.POST.get('txtNombreN','').strip()
    apellido = request.POST.get('txtApellidoN','').strip()
    telefono = request.POST.get('txtTelefonoN','').strip()
    correo = request.POST.get('txtCorreoN','').strip()
    password_plano = request.POST.get('txtPasswordN','').strip()
    tipo_rol = request.POST.get('txtRol')
    vista = request.POST.get('txtVista')


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
        if vista:
            return render(request,'crearCliente.html',contexto)
        return render(request,'registro.html',contexto)
    
    try: 
        #Verificacion de correo y telefono existente
        correoExistente = Usuario.objects.filter(Q(correo_usuario = correo))
        telefonoExistente = Usuario.objects.filter(Q(telefono_usuario = telefono))
        if correoExistente and telefonoExistente:
            contexto['error_correo'] = 'Correo Ya Registrador'
            contexto['error_telefono'] = 'Telefono Ya Registrador'
            if vista:
                return render(request,'crearCliente.html',contexto)
            return render(request,'registro.html',contexto)
        elif correoExistente:
            contexto['error_correo'] = 'Correo Ya Registrador'
            if vista:
                return render(request,'crearCliente.html',contexto)
            return render(request,'registro.html',contexto)
        elif telefonoExistente: 
            contexto['error_telefono'] = 'Telefono Ya Registrador'
            if vista:
                return render(request,'crearCliente.html',contexto)
            return render(request,'registro.html',contexto)
            

        #Cifrador de Contraseña
        password = make_password(password_plano)

        rol = Rol.objects.get(nombre_rol = tipo_rol)

        #Creacion de registro en tabla Usuario de Tipo Cliente
        cliente = Usuario(
            id_rol = rol,
            nombre_usuario = nombre,
            apellido_usuario = apellido,
            correo_usuario = correo,
            password_usuario = password,
            telefono_usuario = telefono,
            usuario_activo = True
        )

        cliente.save()
        if vista:
            #Vista Administraccion
            messages.success(request,'creado')
            return redirect('vista_clientes_administracion')
        #Session para guardar informacion del cliente
        request.session['nombre_cliente'] = cliente.nombre_usuario
        request.session['apellido_cliente'] = cliente.apellido_usuario
        request.session['correo_cliente'] = cliente.correo_usuario
        request.session['id_usuario'] = cliente.id_usuario
        request.session['activo'] = True
        return redirect('vista_inicio_cliente')

    except Exception:
        contexto.clear()
        contexto['error_interno'] = '!Error Interno!'
        return render(request,'registro.html',contexto)
    
# Editar_Perfil_Cliente, logica para editar una cuenta tipo cliente
def Editar_Perfil_Cliente(request):
    imagen = request.FILES.get('imagen_usuario')
    nombre = request.POST.get('txtNombreA','').strip()
    apellido = request.POST.get('txtApellidoA','').strip()
    correo = request.POST.get('txtCorreoA','').strip()
    telefono = request.POST.get('txtTelefonoA','').strip()

    campos_vacios = []
    if not nombre:
        campos_vacios.append('nombre')
    if not apellido:
        campos_vacios.append('apellido')
    if not telefono:
        campos_vacios.append('telefono')
    if not correo:
        campos_vacios.append('correo')

    contexto = {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'correo': correo,
            'campos_vacios': campos_vacios
    }

    try:
        #Obteniendo Cliente
        cliente = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))

        if campos_vacios:
                contexto['activo'] = True
                contexto['usuario'] = cliente
                return render(request,'editar_perfilCliente.html',contexto)
    
        #Actualziacion
        cliente.nombre_usuario = nombre
        cliente.apellido_usuario = apellido
        cliente.telefono_usuario = telefono
        cliente.correo_usuario = correo
        if imagen:
            cliente.imagen_usuario = imagen
        cliente.save()
        #Actualizacion de session
        request.session['nombre_cliente'] = cliente.nombre_usuario
        request.session['apellido_cliente'] = cliente.apellido_usuario
        request.session['correo_cliente'] = cliente.correo_usuario
        return redirect('vista_perfil_cliente')
    except Usuario.DoesNotExist:
        return redirect('vista_login')

def guardar_comentario(request):
    if request.method == 'POST':
        id_cliente = request.session.get('id_usuario', None)

        if id_cliente is None:
            messages.error(request, 'Debes iniciar sesión para comentar.')
            return redirect('vista_login')

        titulo = request.POST.get('titulo')
        comentario = request.POST.get('comentario')

        # Zona horaria manual UTC-6 (El Salvador)
        utc_minus_6 = dt_timezone(timedelta(hours=-6))
        fecha = datetime.now(utc_minus_6).date()  # Solo la fecha (porque es DateField)

        try:
            id_usuario = Usuario.objects.get(id_usuario=id_cliente)

            Comentario.objects.create(
                id_usuario=id_usuario,
                titulo_comentario=titulo,
                comentario=comentario,
                fecha_comentario=fecha
            )
            messages.success(request, '¡Comentario enviado exitosamente!')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no válido.')

    return redirect('vista_comentario')


def RealizarCompra(request):
    correo = request.POST.get('txtCorreo')
    fecha = timezone.localtime(timezone.now()).date()
    total = request.POST.get('txtTotal')
    ids = (request.POST.get('productos[]') or '')
    cantidades = (request.POST.get('cantidades[]') or '')

    lista_ids = [int(i) for i in ids.split(',') if i.strip().isdigit()]
    lista_cantidades = [int(i) for i in cantidades.split(',') if i.strip().isdigit()]

    try:
        usuario = Usuario.objects.get(correo_usuario=correo)
        with transaction.atomic():  # todo o nada
            # Compra
            compra = Compra(
                id_usuario=usuario,
                fecha_compra=fecha,
                total_compra=total
            )
            compra.save()

            # Registrar detalles y descontar stock
            for producto_id, cantidad in zip(lista_ids, lista_cantidades):
                try:
                    producto = Producto.objects.get(id_producto=producto_id)

                    Detalle_Compra.objects.create(
                        id_compra=compra,
                        id_producto=producto,
                        cantidad_producto_compra=cantidad,
                        precio_unitario_compra=producto.precio_producto
                    )

                    # ⬇️ Descontar existencias en DB (campo correcto: existencia_producto)
                    Producto.objects.filter(id_producto=producto_id)\
                        .update(existencia_producto=F('existencia_producto') - cantidad)

                except Producto.DoesNotExist:
                    # Si algún producto no existe, simplemente lo omites
                    pass

            # Comprobante
            cod_comprobante = f"CP-{uuid.uuid4().hex[:12].upper()}"
            Comprobante_Pago.objects.create(
                id_compra=compra,
                fecha_comprobante=fecha,
                codigo_comprobante=cod_comprobante,
                estado_comprobante='Pe',
            )

        messages.success(request, 'exito')
        return redirect('vista_inicio_cliente')

    except Usuario.DoesNotExist:
        return redirect('vista_carrito')
    
#logica para actualizar contraseña
def ActualizarClaveCliente(request):
    correo = request.POST.get('txtCorreo','').strip()
    password = request.POST.get('txtPasswordActual','').strip()
    passwordNueva = request.POST.get('txtPasswordNueva','').strip()
    try:
        usuario = Usuario.objects.get(correo_usuario = correo)
        if check_password(password,usuario.password_usuario):
            nuevaPassword = make_password(passwordNueva)
            usuario.password_usuario = nuevaPassword
            usuario.save()
            messages.success(request,'Exito')
            return redirect('vista_configuracion')
        else:
            messages.warning(request,'Contraseña Invalida') 
            return redirect('vista_configuracion')
    except Usuario.DoesNotExist:
        messages.error(request,'Error')
        return redirect('vista_inicio_cliente')
    
#Logica para desactivar cuenta
def DesactivarCuenta(request):
    correo = request.POST.get('txtCorreo','').strip()
    try:
        usuario = Usuario.objects.get(correo_usuario = correo)
        usuario.usuario_activo = False
        usuario.save()
        del request.session['nombre_cliente']
        del request.session['apellido_cliente']
        del request.session['correo_cliente']
        del request.session['id_usuario']
        del request.session['activo']
        return redirect('vista_inicio_cliente')
    except Usuario.DoesNotExist:
        return redirect('vista_inicio_cliente')
    
# Logica Para registrar un servicio
def RegistrarServicio(request):
    activo = request.session.get('activo',False)
    id_usuario = request.session.get('id_usuario','')
    id_categoria = request.POST.get('categoriaServicio','').strip()
    descripcion = request.POST.get('descripcion','').strip()
    fecha = timezone.localtime(timezone.now()).date()


    if activo:
        #Registro de Servicio
        categoria = Categoria_Servicio.objects.get(id_categoria_servicio = id_categoria)
        usuario = Usuario.objects.get(id_usuario = id_usuario)
        pedido = Servicio(
            id_usuario = usuario,
            id_categoria_servicio = categoria,
            descripcion_servicio = descripcion,
            estado_servicio = 'Re',
            fecha_servicio = fecha,
            comentario_servicio = ''
        )
        pedido.save()
        return redirect('vista_inicio_cliente')
    else:
        return redirect('vista_inicio_cliente')
    