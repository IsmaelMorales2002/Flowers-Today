from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
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

#Funcion Vista_Inicio, Muestra la vista Inicio.html
def Vista_Inicio(request):
    activo = request.session.get('usuario_correo',None)
    if activo:
        return render(request,'inicio.html',{
            'activo': activo
        })
    return render(request,'inicio.html')

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

# Funcion Vista_Listar_Categoria, Muestra la vista listar_categoria.html
# Esta vista lista todas las categorias disponibles en la base de datos
def Vista_Listar_Categoria(request):
    #Seguridad De Ruta
    activo_admin = request.session.get('admin_correo',None)
    if activo_admin:
        try:
            categorias = Categoria.objects.all().order_by('nombre_categoria')
            return render(request, 'listar_categoria.html', {
                'categorias': categorias,
                'activo_admin': activo_admin
            })
        except Exception as e:
            print(e)
            return render(request, 'listar_categoria.html', {'categorias': []})
    return redirect('login')
    
# Funcion Vista_Insertar_Categoria, Muestra la vista insertar_categoria.html
# Esta vista permite al usuario registrar una nueva categoria en la base de datos 
def Vista_Insertar_Categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria', '').strip()

        if nombre_categoria == '':
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
            return redirect('insertar_categoria')

        # Validar duplicado
        if Categoria.objects.filter(nombre_categoria__iexact=nombre_categoria).exists():
            messages.error(request, 'Ya existe una categoría con ese nombre.')
            return redirect('insertar_categoria')

        try:
            nueva_categoria = Categoria(nombre_categoria=nombre_categoria)
            nueva_categoria.save()
            messages.success(request, 'Categoría registrada exitosamente.')
            return redirect('listar_categoria')  # Redirigir a la lista
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar la categoría: {str(e)}')
            return redirect('insertar_categoria')

    return render(request, 'insertar_categoria.html')


def Vista_Insertar_Producto(request):
    categorias = Categoria.objects.all().order_by('nombre_categoria')

    if request.method == 'POST':
        try:
            nombre_producto = request.POST.get('nombre_producto', '').strip()
            id_categoria = request.POST.get('id_categoria')
            descripcion_producto = request.POST.get('descripcion_producto', '').strip()
            
            # Usamos la URL predefinida
            imagen_producto = 'https://acortar.link/zPqL3t'

            cantidad_maxima = request.POST.get('cantidad_maxima')
            cantidad_minima = request.POST.get('cantidad_minima')
            precio_producto = request.POST.get('precio_producto')
            
            existencia_producto = request.POST.get('existencia_producto')
            
            tipo_producto = request.POST.get('tipo_producto')
            
            # Checkbox
            activo = True if request.POST.get('producto_activo') else False

            # Validación básica
            if nombre_producto == '' or id_categoria == '' or tipo_producto == '':
                messages.error(request, 'Debe completar todos los campos.')
                return redirect('insertar_producto')

            nuevo_producto = Producto(
                nombre_producto = nombre_producto,
                id_categoria_id = id_categoria,
                descripcion_producto = descripcion_producto,
                imagen_producto = imagen_producto,
                cantidad_maxima = cantidad_maxima,
                cantidad_minima = cantidad_minima,
                precio_producto = precio_producto,
                existencia_producto = existencia_producto,  # respetando el modelo
                tipo_producto = tipo_producto,
                producto_activo = activo
            )
            nuevo_producto.save()

            messages.success(request, 'Producto registrado exitosamente.')
            return redirect('listar_producto')

        except Exception as e:
            messages.error(request, f'Error al registrar el producto: {str(e)}')
            return redirect('insertar_producto')

    return render(request, 'insertar_producto.html', {'categorias': categorias})


TIPO_PRODUCTO = {
    1: 'Arreglos Mixto',
    2: 'Flores',
    3: 'Arreglos Flores'
}

def Vista_Listar_Producto(request):
    productos = Producto.objects.select_related('id_categoria').all().order_by('-id_producto')
    categorias = Categoria.objects.all().order_by('nombre_categoria')

    lista_productos = []
    for p in productos:
        lista_productos.append({
            'id_producto': p.id_producto,
            'nombre_producto': p.nombre_producto,
            'nombre_categoria': p.id_categoria.nombre_categoria if p.id_categoria else '',
            'id_categoria': p.id_categoria.id_categoria if p.id_categoria else '',
            'tipo_producto': TIPO_PRODUCTO.get(p.tipo_producto, 'Desconocido'),
            'tipo_producto_val': p.tipo_producto,
            'descripcion_producto': p.descripcion_producto,
            'cantidad_maxima': p.cantidad_maxima,
            'cantidad_minima': p.cantidad_minima,
            'precio_producto': p.precio_producto,
            'existencia_producto': p.existencia_producto,
            'producto_activo': p.producto_activo,
            'imagen_producto': p.imagen_producto,  # ya es URL
        })

    return render(request, 'listar_producto.html', {
        'productos': lista_productos,
        'categorias': categorias
    })


def Vista_Editar_Producto(request):
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('id_producto')
            producto = get_object_or_404(Producto, id_producto=id_producto)

            nombre_producto = request.POST.get('nombre_producto', '').strip()
            id_categoria = request.POST.get('id_categoria')
            tipo_producto = request.POST.get('tipo_producto')
            descripcion_producto = request.POST.get('descripcion_producto', '').strip()
            cantidad_maxima = request.POST.get('cantidad_maxima')
            cantidad_minima = request.POST.get('cantidad_minima')
            precio_producto = request.POST.get('precio_producto')
            existencia_producto = request.POST.get('existencia_producto')
            imagen_producto = request.POST.get('imagen_producto', '').strip()
            producto_activo = True if request.POST.get('producto_activo') == 'on' else False

            #  Validación: ningún campo vacío
            if (not nombre_producto or not id_categoria or not tipo_producto or not descripcion_producto 
                or not cantidad_maxima or not cantidad_minima or not precio_producto or not existencia_producto 
                ):
                
                messages.error(request, 'Debe completar todos los campos.')
                return redirect('listar_producto')

            # Si todo bien: actualizar
            producto.nombre_producto = nombre_producto
            producto.id_categoria_id = id_categoria
            producto.tipo_producto = tipo_producto
            producto.descripcion_producto = descripcion_producto
            producto.cantidad_maxima = cantidad_maxima
            producto.cantidad_minima = cantidad_minima
            producto.precio_producto = precio_producto
            producto.existencia_producto = existencia_producto
            producto.imagen_producto = producto.imagen_producto
            producto.producto_activo = producto_activo

            producto.save()

            messages.success(request, 'Producto editado correctamente.')
            return redirect('listar_producto')

        except Exception as e:
            messages.error(request, f'Error al editar producto: {str(e)}')
            return redirect('listar_producto')
    else:
        messages.error(request, 'Método no permitido.')
        return redirect('listar_producto')
    
    
def Vista_Cambiar_Estado_Producto(request):
    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        accion = request.POST.get('accion')  # puede ser 'activar' o 'desactivar'

        producto = get_object_or_404(Producto, id_producto=id_producto)

        if accion == 'activar':
            producto.producto_activo = True
        else:
            producto.producto_activo = False

        producto.save()
        messages.success(request, 'Estado del producto actualizado correctamente.')
        return redirect('listar_producto')
    else:
        messages.error(request, 'Solicitud inválida.')
        return redirect('listar_producto')

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

def Vista_Verificar_Categoria_Existente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_categoria')
        id_categoria = request.POST.get('id_categoria')

        existe = Categoria.objects.filter(nombre_categoria__iexact=nombre).exclude(id_categoria=id_categoria).exists()


        return JsonResponse({'existe': existe})
    return JsonResponse({'existe': False})

# Vista para actualizar el nombre de la categoría
def Vista_Actualizar_Categoria(request):
    if request.method == 'POST':
        id_categoria = request.POST.get('id_categoria')
        nombre_categoria = request.POST.get('nombre_categoria')

        try:
            categoria = Categoria.objects.get(id_categoria=id_categoria)
            categoria.nombre_categoria = nombre_categoria
            categoria.save()
            return JsonResponse({'ok': True})
        except Categoria.DoesNotExist:
            return JsonResponse({'ok': False})
    return JsonResponse({'ok': False})

def cambiar_estado_categoria(request):
    if request.method == 'POST':
        id_categoria = request.POST.get('id_categoria')
        accion = request.POST.get('accion')

        categoria = Categoria.objects.get(id_categoria=id_categoria)
        if accion == 'activar':
            categoria.estado_categoria = True
        else:
            categoria.estado_categoria = False
        categoria.save()

        messages.success(request, 'El estado de la categoría ha sido actualizado.')
        return redirect('listar_categoria')

