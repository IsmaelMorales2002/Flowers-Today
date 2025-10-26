from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from decimal import Decimal

def Crear_Cuenta_Admi(request):
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
            return render(request,'crearAdmi.html',contexto)
        return render(request,'registro.html',contexto)
    
    try: 
        #Verificacion de correo y telefono existente
        correoExistente = Usuario.objects.filter(Q(correo_usuario__iexact = correo)).exists()
        telefonoExistente = Usuario.objects.filter(Q(telefono_usuario = telefono))
        if correoExistente and telefonoExistente:
            contexto['error_correo'] = 'Correo Ya Registrador'
            contexto['error_telefono'] = 'Telefono Ya Registrador'
            if vista:
                return render(request,'crearAdmi.html',contexto)
            return render(request,'registro.html',contexto)
        elif correoExistente:
            contexto['error_correo'] = 'Correo Ya Registrador'
            if vista:
                return render(request,'crearAdmi.html',contexto)
            return render(request,'registro.html',contexto)
        elif telefonoExistente: 
            contexto['error_telefono'] = 'Telefono Ya Registrador'
            if vista:
                return render(request,'crearAdmi.html',contexto)
            return render(request,'registro.html',contexto)
            

        #Cifrador de Contraseña
        password = make_password(password_plano)

        rol = Rol.objects.get(nombre_rol = tipo_rol)

        #Creacion de registro en tabla Usuario de Tipo Cliente
        admi = Usuario(
            id_rol = rol,
            nombre_usuario = nombre,
            apellido_usuario = apellido,
            correo_usuario = correo,
            password_usuario = password,
            telefono_usuario = telefono,
            usuario_activo = True
        )

        admi.save()
        messages.success(request, '¡Administrador creado exitosamente!')

       
        if vista:
            return redirect('vista_administradores_administracion')
        return redirect('vista_inicio_cliente')

    except Exception:
        contexto.clear()
        contexto['error_interno'] = '!Error Interno!'
        return render(request,'registro.html',contexto)
    
    
    
    
    
def Crear_Categoria(request):
    nombre = request.POST.get('txtNombreN', '').strip()
    vista = request.POST.get('txtVista')

    campos_vacios = []
    if not nombre:
        campos_vacios.append('nombre')

    contexto = {
        'nombre': nombre,
        'campos_vacios': campos_vacios
    }

    if campos_vacios:
        if vista:
            return render(request, 'crearCategoria.html', contexto)
        return render(request, 'registro.html', contexto)
    
    

    try:
       
        nombreExiste = Categoria.objects.filter(nombre_categoria__iexact=nombre).exists()
        if nombreExiste:
            contexto['error_nombre'] = 'Nombre Ya Registrado'
            if vista:
                return render(request, 'crearCategoria.html', contexto)
            return render(request, 'registro.html', contexto)

        # Crear nueva categoría
        categoria = Categoria(
            nombre_categoria=nombre,
            estado_categoria=True
        )
        categoria.save()
        messages.success(request, 'Categoría creada exitosamente')

        if vista:
            return redirect('vista_categoria_administracion')
        return redirect('vista_inicio_cliente')

    except Exception:
  
        contexto['error_interno'] = '!Error Interno!'
        return render(request, 'crearCategoria.html', contexto)

#Crear Categoria De Servicio
def Crear_Categoria_Servicio(request):
    nombre = request.POST.get('txtNombreN', '').strip()
    vista = request.POST.get('txtVista')

    campos_vacios = []
    if not nombre:
        campos_vacios.append('nombre')

    contexto = {
        'nombre': nombre,
        'campos_vacios': campos_vacios
    }

    if campos_vacios:
        if vista:
            return render(request, 'crearCategoriaServicio.html', contexto)
        return render(request, 'registro.html', contexto)
    
    try:
       
        nombreExiste = Categoria_Servicio.objects.filter(nombre_categoria_servicio__iexact=nombre).exists()
        if nombreExiste:
            contexto['error_nombre'] = 'Nombre Ya Registrado'
            if vista:
                return render(request, 'crearCategoriaServicio.html', contexto)
            return render(request, 'registro.html', contexto)

        # Crear nueva categoría
        categoriaServicio = Categoria_Servicio(
            nombre_categoria_servicio=nombre,
            estado_categoria_servicio=True
        )
        categoriaServicio.save()
        messages.success(request, 'Categoría creada exitosamente')

        if vista:
            return redirect('vista_categoria_servicio')
        return redirect('vista_inicio_cliente')

    except Exception:
  
        contexto['error_interno'] = '!Error Interno!'
        return render(request, 'crearCategoriaServicio.html', contexto)


def Editar_Categoria(request, id_categoria):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombreN', '').strip()
        campos_vacios = []
        error_nombre = False
        error_longitud = False

        if not nombre:
            campos_vacios.append('nombre')
        if len(nombre) > 25:
            error_longitud = True

        contexto = {
            'nombre': nombre,
            'campos_vacios': campos_vacios,
            'error_nombre': False,
            'error_longitud': error_longitud,
            'id_categoria': id_categoria  # <- Esto es crucial
        }

        if campos_vacios or error_longitud:
            return render(request, 'editar_categoria.html', contexto)

        try:
            # Verificar si ya existe otra categoria con ese nombre, excluyendo la actual
            existe = Categoria.objects.filter(nombre_categoria__iexact=nombre).exclude(id_categoria=id_categoria).exists()
            if existe:
                contexto['error_nombre'] = True
                return render(request, 'editar_categoria.html', contexto)

            categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
            categoria.nombre_categoria = nombre
            categoria.save()
            messages.success(request, 'categoria_editada')

            return redirect('vista_categoria_administracion')
        except Exception:
            contexto['error_interno'] = '!Error interno!'
            return render(request, 'editar_categoria.html', contexto)

# Editar Categoria Servicio
def Editar_CategoriaServicio(request, id_categoria_servicio):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombreN', '').strip()
        campos_vacios = []
        error_nombre = False
        error_longitud = False

        if not nombre:
            campos_vacios.append('nombre')
        if len(nombre) > 25:
            error_longitud = True

        contexto = {
            'nombre': nombre,
            'campos_vacios': campos_vacios,
            'error_nombre': False,
            'error_longitud': error_longitud,
            'id_categoria_servicio': id_categoria_servicio  # <- Esto es crucial
        }

        if campos_vacios or error_longitud:
            return render(request, 'editar_categoriaServicio.html', contexto)

        try:
            # Verificar si ya existe otra categoria con ese nombre, excluyendo la actual
            existe = Categoria_Servicio.objects.filter(nombre_categoria_servicio__iexact=nombre).exclude(id_categoria_servicio=id_categoria_servicio).exists()
            if existe:
                contexto['error_nombre'] = True
                return render(request, 'editar_categoriaServicio.html', contexto)

            categoria = get_object_or_404(Categoria_Servicio, id_categoria_servicio=id_categoria_servicio)
            categoria.nombre_categoria_servicio = nombre
            categoria.save()
            messages.success(request, 'categoria_editada')

            return redirect('vista_categoria_servicio')
        except Exception:
            contexto['error_interno'] = '!Error interno!'
            return render(request, 'editar_categoriaServicio.html', contexto)

def cambiar_estado_categoria(request):
    if request.method == 'POST':
        id_categoria = request.POST.get('id_categoria')
        accion = request.POST.get('accion')

        try:
            categoria = Categoria.objects.get(id_categoria=id_categoria)
            if accion == 'desactivar':
                categoria.estado_categoria = False
            elif accion == 'activar':
                categoria.estado_categoria = True
            categoria.save()
        except Categoria.DoesNotExist:
            pass

    return redirect('vista_categoria_administracion')  # Ajusta a tu vista real



def Editar_Cuenta_Admi(request, id):
    # Protección de ruta: verificar sesión de administrador activo
    activo = request.session.get('activo_administrador', False)
    if not activo:
        return redirect('vista_inicio_cliente')  # o a donde quieras redirigir si no está activo

    try:
        administrador = Usuario.objects.get(id_usuario=id)
    except Usuario.DoesNotExist:
        return redirect('vista_administradores_administracion')

    if request.method == 'POST':
        nombre = request.POST.get('txtNombre', '').strip()
        apellido = request.POST.get('txtApellido', '').strip()
        telefono = request.POST.get('txtTelefono', '').strip()
        correo = request.POST.get('txtCorreo', '').strip()
        rol = request.POST.get('txtRol', '').strip()

        campos_vacios = []
        if not nombre: campos_vacios.append('nombre')
        if not apellido: campos_vacios.append('apellido')
        if not telefono: campos_vacios.append('telefono')
        if not correo: campos_vacios.append('correo')
        if not rol: campos_vacios.append('rol')

        contexto = {
            'administrador': administrador,
            'campos_vacios': campos_vacios,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'correo': correo,
            'rol': rol,
            'activo': activo,  # para el template si usas este dato
        }

        if campos_vacios:
            return render(request, 'editarAdmi.html', contexto)

        if Usuario.objects.filter(correo_usuario=correo).exclude(id_usuario=id).exists():
            contexto['error_correo'] = 'El correo ya está en uso.'
            return render(request, 'editarAdmi.html', contexto)

        if Usuario.objects.filter(telefono_usuario=telefono).exclude(id_usuario=id).exists():
            contexto['error_telefono'] = 'El teléfono ya está en uso.'
            return render(request, 'editarAdmi.html', contexto)

        try:
            nuevo_rol = Rol.objects.get(nombre_rol=rol)
        except Rol.DoesNotExist:
            contexto['error_rol'] = 'El rol seleccionado no es válido.'
            return render(request, 'editarAdmi.html', contexto)

        administrador.nombre_usuario = nombre
        administrador.apellido_usuario = apellido
        administrador.correo_usuario = correo
        administrador.telefono_usuario = telefono
        administrador.id_rol = nuevo_rol
        administrador.save()

        messages.success(request, 'editado')
        return redirect('vista_administradores_administracion')

    # Si no es POST, mostrar datos actuales con validación de sesión
    return render(request, 'editarAdmi.html', {
        'administrador': administrador,
        'activo': activo
    })

# Editar_Cuenta_Cliente, logica para editar cuenta de cliente desde el administrador
def Editar_Cuenta_Cliente(request,id):
    # Proteccion de ruta
    activo = request.session.get('activo_administrador', False)
    if not activo:
        return redirect('vista_inicio_cliente')
    
    try:
        cliente = Usuario.objects.get(id_usuario = id)
    except Usuario.DoesNotExist:
        return redirect('vista_clientes_administracion')
    
    nombre = request.POST.get('txtNombreCA', '').strip()
    apellido = request.POST.get('txtApellidoCA', '').strip()
    telefono = request.POST.get('txtTelefonoCA', '').strip()
    correo = request.POST.get('txtCorreoCA', '').strip()
    rol = request.POST.get('txtRolCA', '').strip()

    campos_vacios = []
    if not nombre: campos_vacios.append('nombre')
    if not apellido: campos_vacios.append('apellido')
    if not telefono: campos_vacios.append('telefono')
    if not correo: campos_vacios.append('correo')
    if not rol: campos_vacios.append('rol')

    contexto = {
        'cliente': cliente,
        'campos_vacios': campos_vacios,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'correo': correo,
        'rol': rol,
    }

    if campos_vacios:
            return render(request, 'editarCliente.html', contexto)
    
    if Usuario.objects.filter(correo_usuario=correo).exclude(id_usuario=id).exists():
        contexto['error_correo'] = 'El correo ya está en uso.'
        return render(request,'editarCliente.html',contexto)
    
    if Usuario.objects.filter(telefono_usuario=telefono).exclude(id_usuario=id).exists():
        contexto['error_telefono'] = 'El teléfono ya está en uso.'
        return render(request,'editarCliente.html',contexto)
    
    try:
        nuevo_rol = Rol.objects.get(nombre_rol = rol)
    except Rol.DoesNotExist:
        contexto['error_rol'] = 'El rol seleccionado no es válido'
        return render(request,'editarCliente.html',contexto)
    
    cliente.nombre_usuario = nombre
    cliente.apellido_usuario = apellido
    cliente.correo_usuario = correo
    cliente.telefono_usuario = telefono
    cliente.id_rol = nuevo_rol
    cliente.save()

    messages.success(request,'editado')
    return redirect('vista_clientes_administracion')


def cambiar_estado_administrador(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        accion = request.POST.get('accion')

        try:
            administrador = Usuario.objects.get(id_usuario=id_usuario)
            if accion == 'desactivar':
                administrador.usuario_activo = False
            elif accion == 'activar':
                administrador.usuario_activo = True
            administrador.save()
        except Usuario.DoesNotExist:
            pass

    return redirect('vista_administradores_administracion')


#Logica para cambiar estado de cuenta cliente
def cambiar_estado_Cliente(request):
    id_usuario = request.POST.get('id_usuario')
    accion = request.POST.get('accion')
    try:
        cliente = Usuario.objects.get(id_usuario=id_usuario)
        if accion == 'desactivar':
            cliente.usuario_activo = False
        elif accion == 'activar':
            cliente.usuario_activo = True
        cliente.save()
        return redirect('vista_clientes_administracion')
    except Usuario.DoesNotExist:
        pass

#Logica para cambiar estado producto
def Cambiar_Estado_Producto(request):
    id_producto = request.POST.get('id_producto','')
    accion = request.POST.get('accion')
    try:
        producto = Producto.objects.get(id_producto = id_producto)
        if accion == 'desactivar':
            producto.producto_activo = False
        elif accion == 'activar':
            producto.producto_activo = True
        producto.save()
        return redirect('vista_productos_administracion')
    except Producto.DoesNotExist:
        pass

#Logica para crear producto
def Crear_Producto(request):
    nombre_producto = request.POST.get('nombre_producto','').strip()
    descripcion_producto = request.POST.get('descripcion_producto','').strip()
    cantidad_maxima = request.POST.get('cantidad_maxima','').strip()
    cantidad_minima = request.POST.get('cantidad_minima','').strip()
    precio_producto = request.POST.get('precio_producto','').strip()
    existencia_producto = request.POST.get('existencia_producto','').strip()
    tipo_producto = request.POST.get('tipo_producto','').strip()
    producto_activo = request.POST.get('producto_activo')
    id_categoria = request.POST.get('id_categoria','').strip()
    imagen_producto = request.FILES.get('imagen_producto')

    campos_vacios = []
    if not nombre_producto: campos_vacios.append('nombre_producto')
    if not descripcion_producto: campos_vacios.append('descripcion_producto')
    if not cantidad_maxima: campos_vacios.append('cantidad_maxima')
    if not cantidad_minima: campos_vacios.append('cantidad_minima')
    if not precio_producto: campos_vacios.append('precio_producto')
    if not existencia_producto: campos_vacios.append('existencia_producto')
    if not tipo_producto: campos_vacios.append('tipo_producto')
    if not id_categoria: campos_vacios.append('id_categoria')

    categorias = Categoria.objects.all()
    contexto = {
        'nombre_producto': nombre_producto,
        'descripcion_producto': descripcion_producto,
        'cantidad_maxima': cantidad_maxima,
        'cantidad_minima': cantidad_minima,
        'precio_producto': precio_producto,
        'existencia_producto': existencia_producto,
        'tipo_producto': tipo_producto,
        'id_categoria': id_categoria,
        'categorias': categorias,
        'campos_vacios': campos_vacios
    }

    if campos_vacios:
        return render(request,'agregar_producto.html',contexto)
    
    if Producto.objects.filter(nombre_producto=nombre_producto).exists():
        contexto['error_nombre'] = 'Ya existe un producto con este nombre'
        return render(request,'agregar_producto.html',contexto)
    
    try:
        categoria = Categoria.objects.get(id_categoria = id_categoria)
        ## Conversiones de texto a decimales o entero
        cantMx = int(cantidad_maxima)
        cantMn = int(cantidad_minima)
        precio = Decimal(precio_producto)
        existencia = int(existencia_producto)
        activo = True if producto_activo == 'on' else False
        producto = Producto(
            id_categoria = categoria,
            nombre_producto = nombre_producto,
            descripcion_producto = descripcion_producto,
            imagen_producto = imagen_producto,
            cantidad_maxima = cantMx,
            cantidad_minima = cantMn,
            precio_producto = precio,
            existencia_producto = existencia,
            tipo_producto = tipo_producto,
            producto_activo = activo
        )
        producto.save()
        messages.success(request,'creado')
        return redirect('vista_productos_administracion')
    except Categoria.DoesNotExist:
        messages.error(request,'!Error, No se pudo registrar el producto!')
        return redirect('vista_productos_administracion')

def listar_pedidos():
    return Comprobante_Pago.objects.all()

def cambiar_estado_pedido(request):
    id_comprobante = request.POST.get('id_comprobante')
    comprobante = get_object_or_404(Comprobante_Pago, id_comprobante=id_comprobante)
    
    # Cambiar estado a 'Pa' (pagado)
    comprobante.estado_comprobante = 'Pa'
    comprobante.save()
    
#Logica Para Editar Producto
def Editar_Producto(request,id):
    nombre_producto = request.POST.get('nombre_producto','').strip()
    descripcion_producto = request.POST.get('descripcion_producto','').strip()
    cantidad_maxima = request.POST.get('cantidad_maxima','').strip()
    cantidad_minima = request.POST.get('cantidad_minima','').strip()
    precio_producto = request.POST.get('precio_producto','').strip()
    existencia_producto = request.POST.get('existencia_producto','').strip()
    tipo_producto = request.POST.get('tipo_producto','').strip()
    producto_activo = request.POST.get('producto_activo')
    id_categoria = request.POST.get('id_categoria','').strip()
    imagen_producto = request.FILES.get('imagen_producto')

    #Verificacion de producto existente
    try:
        producto = Producto.objects.get(id_producto = id)
    except Producto.DoesNotExist:
        return redirect('vista_productos_administracion')

    campos_vacios = []
    if not nombre_producto: campos_vacios.append('nombre_producto')
    if not descripcion_producto: campos_vacios.append('descripcion_producto')
    if not cantidad_maxima: campos_vacios.append('cantidad_maxima')
    if not cantidad_minima: campos_vacios.append('cantidad_minima')
    if not precio_producto: campos_vacios.append('precio_producto')
    if not existencia_producto: campos_vacios.append('existencia_producto')
    if not tipo_producto: campos_vacios.append('tipo_producto')
    if not id_categoria: campos_vacios.append('id_categoria')

    categorias = Categoria.objects.all()
    contexto = {
        'producto': producto,
        'nombre_producto': nombre_producto,
        'descripcion_producto': descripcion_producto,
        'cantidad_maxima': cantidad_maxima,
        'cantidad_minima': cantidad_minima,
        'precio_producto': precio_producto,
        'existencia_producto': existencia_producto,
        'tipo_producto': tipo_producto,
        'id_categoria': id_categoria,
        'categorias': categorias,
        'campos_vacios': campos_vacios
    }

    if campos_vacios:
        return render(request,'editar_producto.html',contexto)
    
    # Verificacion de nombre
    if Producto.objects.filter(nombre_producto=nombre_producto).exclude(id_producto = id).exists():
        contexto['error_nombre'] = 'Nombre Ya Registrado'
        return render(request,'editar_producto.html',contexto)
    
    categoria = Categoria.objects.get(id_categoria = id_categoria)
    activo = True if producto_activo == 'on' else False
    #Actualziacion De Datos
    producto.nombre_producto = nombre_producto
    producto.id_categoria = categoria
    producto.tipo_producto = tipo_producto
    producto.descripcion_producto = descripcion_producto
    producto.cantidad_maxima = cantidad_maxima
    producto.cantidad_minima = cantidad_minima
    producto.precio_producto = Decimal(precio_producto)
    producto.existencia_producto = existencia_producto
    producto.producto_activo = activo
    if imagen_producto:
        producto.imagen_producto = imagen_producto
    producto.save()
    messages.success(request,'editado')
    return redirect('vista_productos_administracion')

# Editar_Perfil_Admin, logica para editar una cuenta tipo cliente
def Editar_Perfil_Admin(request):
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
        admin = Usuario.objects.get(id_usuario = request.session.get('id_usuario',None))

        if campos_vacios:
                contexto['activo'] = True
                contexto['usuario'] = admin
                return render(request,'editar_perfilCliente.html',contexto)
    
        #Actualziacion
        admin.nombre_usuario = nombre
        admin.apellido_usuario = apellido
        admin.telefono_usuario = telefono
        admin.correo_usuario = correo
        if imagen:
            admin.imagen_usuario = imagen
        admin.save()
        #Actualizacion de session
        request.session['nombre_administrador'] = admin.nombre_usuario
        request.session['apellido_administrador'] = admin.apellido_usuario
        request.session['correo_administrador'] = admin.correo_usuario
        return redirect('vista_perfil_administrador')
    except Usuario.DoesNotExist:
        return redirect('vista_login')



