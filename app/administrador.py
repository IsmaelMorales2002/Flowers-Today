from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

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
