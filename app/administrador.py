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