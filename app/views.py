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
from django.http import JsonResponse
#Generacion de Tokens
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import token_generator
from app.generar_comprobante import *
from django.utils import timezone
import datetime, json
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from decimal import Decimal
from django.db.models.functions import TruncMonth, TruncDate
# Vista_Inicio, muestra la vista inicio.html
def Vista_Inicio_Cliente(request):
    # ✅ Solo productos activos con stock
    productos = (Producto.objects
                 .filter(producto_activo=True, existencia_producto__gt=0)
                 .select_related('id_categoria'))

    # ✅ Solo categorías activas que tengan productos activos con stock
    categorias = (Categoria.objects
                  .filter(estado_categoria=True,
                          producto__producto_activo=True,
                          producto__existencia_producto__gt=0)
                  .distinct())

    activo = request.session.get('activo', False)
    return render(request, 'inicio.html', {
        'activo': activo,
        'productos': productos,
        'categorias': categorias
    })
    
    
    
def _first_of_month(d: datetime.date) -> datetime.date:
    return d.replace(day=1)

def _shift_months(d: datetime.date, delta: int) -> datetime.date:
    y = d.year + (d.month - 1 + delta) // 12
    m = (d.month - 1 + delta) % 12 + 1
    return datetime.date(y, m, 1)

def _coerce_date(x):
    return x.date() if hasattr(x, "date") else x


def Vista_Inicio_Administrador(request):
    if not request.session.get('activo_administrador', False):
        return redirect('vista_inicio_cliente')

    hoy_local = timezone.localdate()

    # === KPIs ===
    total_ventas = Compra.objects.aggregate(total=Sum('total_compra'))['total'] or 0
    total_compras = Compra.objects.count()
    ingreso_promedio = (
        Compra.objects.aggregate(prom=Sum('total_compra') / Count('id_compra'))['prom'] or 0
    )

    # === Productos críticos ===
    productos_criticos = (
        Producto.objects.filter(producto_activo=True)
        .annotate(diferencia=F('existencia_producto') - F('cantidad_minima'))
        .filter(diferencia=1)
        .count()
    )

    # === Próximos a agotarse ===
    productos_bajos = (
        Producto.objects.filter(producto_activo=True)
        .annotate(diferencia=F('existencia_producto') - F('cantidad_minima'))
        .filter(diferencia=1)
        .select_related('id_categoria')
        .order_by('existencia_producto', 'cantidad_minima')[:30]
    )

    # === Ventas por mes (últimos 6 meses) ===
    first_this_month = _first_of_month(hoy_local)
    meses = [_shift_months(first_this_month, -i) for i in range(5, -1, -1)]
    inicio_rango = meses[0]
    fin_rango_exclusivo = _shift_months(first_this_month, 1)
    nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                     'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    # TruncMonth sin tzinfo porque es DateField
    ventas_prod_qs = (
        Compra.objects
        .filter(fecha_compra__gte=inicio_rango, fecha_compra__lt=fin_rango_exclusivo)
        .annotate(mes=TruncMonth('fecha_compra'))
        .values('mes')
        .annotate(total=Sum('total_compra'))
        .order_by('mes')
    )
    mapa_prod = {_coerce_date(r['mes']): r['total'] for r in ventas_prod_qs}

    serv_qs = (
        Servicio.objects
        .filter(fecha_servicio__gte=inicio_rango, fecha_servicio__lt=fin_rango_exclusivo)
        .annotate(mes=TruncMonth('fecha_servicio'))
        .values('mes')
        .annotate(total=Count('id_servicio'))
        .order_by('mes')
    )
    mapa_serv = {_coerce_date(r['mes']): r['total'] for r in serv_qs}

    meses_labels = [nombres_meses[m.month - 1] for m in meses]
    ventas_productos_datos = [float(mapa_prod.get(m, Decimal('0')) or 0) for m in meses]
    ventas_servicios_datos = [int(mapa_serv.get(m, 0) or 0) for m in meses]

    # === Semana actual (lun-dom) ===
    inicio_semana = hoy_local - datetime.timedelta(days=hoy_local.weekday())
    fin_semana = inicio_semana + datetime.timedelta(days=6)

    total_semana_actual_val = (
        Compra.objects
        .filter(fecha_compra__gte=inicio_semana, fecha_compra__lte=fin_semana)
        .aggregate(total=Sum('total_compra'))['total'] or Decimal('0')
    )

        # === Últimos 7 días (con días faltantes = 0) ===
    inicio_ultimos7 = hoy_local - datetime.timedelta(days=6)
    # Trae lo que exista en BD
    ventas_dias_qs = (
        Compra.objects
        .filter(fecha_compra__gte=inicio_ultimos7, fecha_compra__lte=hoy_local)
        .values('fecha_compra')
        .annotate(total=Sum('total_compra'))
        .order_by('fecha_compra')
    )
    # Mapa fecha -> total real
    mapa_dias = {v['fecha_compra']: v['total'] for v in ventas_dias_qs}

    # Construye TODOS los 7 días seguidos y rellena con 0
    dias_ultimos7 = [inicio_ultimos7 + datetime.timedelta(days=i) for i in range(7)]
    dias_ultimos7_rows = [
        {'fecha': d.strftime('%d/%m/%Y'), 'total': float(mapa_dias.get(d) or 0)}
        for d in dias_ultimos7
    ]


    # === Estado de comprobantes ===
    estados_qs = (
        Comprobante_Pago.objects
        .filter(estado_comprobante__in=['Pa', 'Pe'])
        .values('estado_comprobante')
        .annotate(total=Count('id_comprobante'))
    )
    mapa_estados = {r['estado_comprobante']: r['total'] for r in estados_qs}
    comp_pagados = int(mapa_estados.get('Pa', 0))
    comp_pendientes = int(mapa_estados.get('Pe', 0))

    # === Top productos ===
    top_qs = (
        Detalle_Compra.objects.values('id_producto__nombre_producto')
        .annotate(
            cantidad_vendida=Sum('cantidad_producto_compra'),
            ingresos=Sum(ExpressionWrapper(
                F('cantidad_producto_compra') * F('precio_unitario_compra'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            ))
        )
        .order_by('-cantidad_vendida')[:5]
    )
    productos_labels = [r['id_producto__nombre_producto'] for r in top_qs]
    productos_ingresos = [float(r['ingresos'] or 0) for r in top_qs]
    productos_cantidades = [int(r['cantidad_vendida'] or 0) for r in top_qs]

    return render(request, 'inicioAdministrador.html', {
        'activo': True,
        'nombre': request.session.get('nombre_administrador', ''),
        'apellido': request.session.get('apellido_administrador', ''),

        'productos_bajos': productos_bajos,
        'kpi_total_ventas': f"${total_ventas:,.2f}",
        'kpi_total_compras': total_compras,
        'kpi_promedio': f"${ingreso_promedio:,.2f}",
        'kpi_criticos': productos_criticos,

        'meses_labels': json.dumps(meses_labels),
        'ventas_productos_datos': json.dumps(ventas_productos_datos),
        'ventas_servicios_datos': json.dumps(ventas_servicios_datos),

        'dias_ultimos7_rows': dias_ultimos7_rows,
        'comp_pagados': comp_pagados,
        'comp_pendientes': comp_pendientes,

        'productos_labels': json.dumps(productos_labels),
        'productos_ingresos': json.dumps(productos_ingresos),
        'productos_cantidades': json.dumps(productos_cantidades),

        'semana_del': inicio_semana.strftime('%d/%m/%Y'),
        'semana_al': fin_semana.strftime('%d/%m/%Y'),
        'total_semana_actual': f"${float(total_semana_actual_val):,.2f}",
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

    contexto = {}
    try: 
        usuario = Usuario.objects.get(correo_usuario = correo)
        
        if usuario.usuario_activo:
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
        else:
            return redirect('vista_inicio_cliente')

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

#Vista de categorias de servicio
def Vista_Categoria_Servicio_Administracion(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    if activo:
        try:
            usuarios = Usuario.objects.filter(id_rol__nombre_rol = 'A')
            categorias = Categoria_Servicio.objects.all()
            
            return render(request,'categoria_servicios.html',{
                'activo' : activo,
                'usuarios': usuarios,
                'categorias': categorias
            })
        except Exception as e:
            return redirect('vista_inicio_administrador')

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

#Vista Crear Categoria Servicio
def Vista_Crear_Categoria_Servicio(request):
    #Proteccion de ruta
    activo = request.session.get('activo_administrador',False)
    
    if activo:
        return render(request,'crearCategoriaServicio.html',{
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

#Vista_Editar_Categoria_Servicio
def Vista_Editar_Categoria_Servicio(request, id_categoria_servicio):
    activo = request.session.get('activo_administrador', False)
    if activo:
        try:
            categoria = Categoria_Servicio.objects.get(id_categoria_servicio=id_categoria_servicio)
            contexto = {
                'activo': activo,
                'nombre': categoria.nombre_categoria_servicio,
                'id_categoria_servicio': id_categoria_servicio
            }
            return render(request, 'editar_categoriaServicio.html', contexto)
        except Categoria.DoesNotExist:
            return redirect('vista_categoria_servicio')

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
            comprobantes = Comprobante_Pago.objects.filter(id_compra__in = compras)

            if request.GET.get('pdf'):
                return generar_comprobante_pdf(request.GET.get('pdf'))

            return render(request,'historial_compras.html',{
                'activo': activo,
                'comprobantes': comprobantes
            })    
        except Compra.DoesNotExist:
            return redirect('vista_inicio_cliente')
    return redirect('vista_inicio_cliente')

#Peticion GET_Consultar_Detalle_Compra
def GET_Detalle_Compra(request,compra_id):
    
    compra = Compra.objects.get(id_compra = compra_id, id_usuario = request.session.get('id_usuario'))
    
    detalles = Detalle_Compra.objects.filter(id_compra = compra.id_compra)
    productos = []

    for detalle in detalles:
        productos.append({
            "nombre": detalle.id_producto.nombre_producto,  
            "imagen": detalle.id_producto.imagen_producto.url if detalle.id_producto.imagen_producto else "/static/img/producto-default.png",
            "cantidad": detalle.cantidad_producto_compra,
            "precio": float(detalle.precio_unitario_compra),
            "subtotal": float(detalle.cantidad_producto_compra * detalle.precio_unitario_compra)
        })

    return JsonResponse({
        "id_compra": compra.id_compra,
        "fecha": compra.fecha_compra,
        "total": compra.total_compra,
        "productos": productos,
    })

#Vista Configuracion
def Vista_Configuracion(request):
    activo = request.session.get('activo',False)
    if activo:
        return render(request,'configuracion.html',{
            'activo': activo
        })
    return redirect('vista_inicio_cliente')

#Vista Arreglos
def Vista_Arreglos(request):
    productos = Producto.objects.filter(producto_activo = True)
    categorias = Categoria.objects.filter(
        estado_categoria=True,
        producto__producto_activo=True,
        nombre_categoria__icontains = 'arreglo'
    ).distinct()
    activo = request.session.get('activo',False)
    return render(request,'arreglos.html',{
        'activo': activo,
        'categorias': categorias,
        'productos': productos
    })

#Vista Flores

def Vista_Flores(request):
    # ✅ Solo productos activos con existencias mayores a 0
    productos = Producto.objects.filter(
        producto_activo=True,
        existencia_producto__gt=0,
        id_categoria__estado_categoria=True  # opcional, evita mostrar productos de categorías inactivas
    )

    # ✅ Solo categorías activas con productos de flores/rosas con existencias > 0
    categorias = Categoria.objects.filter(
        estado_categoria=True,
        producto__producto_activo=True,
        producto__existencia_producto__gt=0
    ).filter(
        Q(nombre_categoria__icontains='flore') |
        Q(nombre_categoria__icontains='rosa')
    ).distinct()

    activo = request.session.get('activo', False)

    return render(request, 'flores.html', {
        'activo': activo,
        'categorias': categorias,
        'productos': productos
    })

# Vista Solicitar Servicio
def Vista_Solicitar_Servicio(request):
    activo = request.session.get('activo',False)
    categoria_servicio = Categoria_Servicio.objects.filter(estado_categoria_servicio = True)
    return render(request,'servicios.html',{
        'activo': activo,
        'categorias': categoria_servicio
    })

#Vista Solicitudes de Pedidos
def Vista_SolicitudesPedidos(request):
    activo = request.session.get('activo',False)
    if activo:
        servicios = Servicio.objects.filter(id_usuario__correo_usuario = request.session.get('correo_cliente'))
        return render(request,'solicitudesPedidos.html',{
            'activo': activo,
            'servicios': servicios
        })
    return redirect('vista_inicio_cliente')

#Vista Solicitudes de Pedidos Administracion
def Vista_Solicitudes_Pedidos_Admin(request):
    activo = request.session.get('activo_administrador',False)
    if activo:
        servicios = Servicio.objects.all()
        return render(request,'solicitudesPedidosAdmin.html',{
            'activo': activo,
            'servicios': servicios
        })
    return redirect('vista_inicio_cliente')
