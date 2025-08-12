import os
import uuid
from django.db import models

#Funcion para crear Nombre Unico a la Imagen
def ruta_unica(instance, filename):
    extension = filename.split('.')[-1]
    return f'uploads/{uuid.uuid4()}.{extension}'


# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True,verbose_name='ID')
    nombre_rol = models.CharField(max_length=2,verbose_name='Rol')

    class Meta:
        db_table = 'Rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return f'ID: {self.id_rol}, Rol: {self.nombre_rol}'
    
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True,verbose_name='ID')
    id_rol = models.ForeignKey(Rol,on_delete=models.RESTRICT)
    nombre_usuario = models.CharField(max_length=50,verbose_name='Nombre')
    apellido_usuario = models.CharField(max_length=50,verbose_name='Apellido')
    correo_usuario = models.CharField(max_length=100,verbose_name='Correo Electronico')
    password_usuario = models.CharField(max_length=150,verbose_name='Contraseña')
    telefono_usuario = models.CharField(max_length=10,verbose_name='Telefono')
    imagen_usuario = models.ImageField(upload_to=ruta_unica,blank=True,verbose_name='Imagen Usuario')
    usuario_activo = models.BooleanField(verbose_name='Cuenta Activa')

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'ID: {self.id_usuario}, Nombre: {self.nombre_usuario}, Apellido: {self.apellido_usuario}, Correo: {self.correo_usuario}'

class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True,verbose_name='ID')
    id_usuario = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    titulo_comentario = models.CharField(max_length=50,verbose_name='Titulo')
    comentario = models.CharField(max_length=200,verbose_name='Comentario')
    fecha_comentario = models.DateField(verbose_name='Fecha')

    class Meta:
        db_table = 'Comentario'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'ID: {self.id_comentario}, Usuario: {self.id_usuario.correo_usuario}, Titulo: {self.titulo_comentario}'
    
class Categoria_Servicio(models.Model):
    id_categoria_servicio = models.AutoField(primary_key=True,verbose_name='ID')
    nombre_categoria_servicio = models.CharField(max_length=25)
    estado_categoria_servicio = models.BooleanField(verbose_name='Estado',default=True)

    class Meta:
        db_table = 'Categoria Servicio'
        verbose_name = 'Categoria Servicio'
        verbose_name_plural = 'Categoria Servicios'

    def __str__(self):
        return f'ID: {self.id_categoria_servicio}, Categoria: {self.nombre_categoria_servicio}'
    
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True,verbose_name='ID')
    nombre_categoria = models.CharField(max_length=25)
    estado_categoria = models.BooleanField(verbose_name='Estado',default=True)

    class Meta:
        db_table = 'Categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return f'ID: {self.id_categoria}, Categoria: {self.nombre_categoria}'

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True,verbose_name='ID')
    id_usuario = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    id_categoria_servicio = models.ForeignKey(Categoria_Servicio,on_delete=models.RESTRICT)
    descripcion_servicio = models.CharField(max_length=150,verbose_name='Descripcion')
    estado_servicio = models.CharField(max_length=2,verbose_name='Estado Servicio')
    fecha_servicio = models.DateField(verbose_name='Fecha Pedido')
    comentario_servicio = models.CharField(max_length=150)

    class Meta:
        db_table = 'Servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return f'ID: {self.id_servicio}, Usuario: {self.id_usuario.correo_usuario}, Fecha: {self.fecha_servicio}'
    
class Producto(models.Model):

    tipo_producto_choides = [
        (1,'Arreglo Flores'),
        (2, 'Arreglo Personalizado'),
        (3, 'Arreglo Mixto')
    ]

    id_producto = models.AutoField(primary_key=True,verbose_name='ID')
    id_categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre_producto = models.CharField(max_length=50,verbose_name='Nombre')
    descripcion_producto = models.CharField(max_length=100,verbose_name='Descripcion')
    imagen_producto = models.ImageField(upload_to=ruta_unica,blank=True,verbose_name='Imagen Producto')
    cantidad_maxima = models.IntegerField(verbose_name='Cantidad Maxina')
    cantidad_minima = models.IntegerField(verbose_name='Cantidad Minima')
    precio_producto = models.DecimalField(max_digits=8,decimal_places=2)
    existencia_producto = models.IntegerField(verbose_name='Existencia')
    tipo_producto = models.IntegerField(choices=tipo_producto_choides,verbose_name='Tipo Producto')
    producto_activo = models.BooleanField(verbose_name='Producto Activo')

    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'ID: {self.id_producto}, Nombre: {self.nombre_producto}'
    

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True,verbose_name='ID')
    id_usuario = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    fecha_compra = models.DateField(verbose_name='Fecha De Compra')
    total_compra = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Total de Compra')

    class Meta:
        db_table = 'Compra'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'ID: {self.id_compra}, Usuario: {self.id_usuario.correo_usuario}, Fecha: {self.fecha_compra}'

class Detalle_Servicio(models.Model):
    id_detalle_servicio = models.AutoField(primary_key=True,verbose_name='ID')
    id_servicio = models.ForeignKey(Servicio,on_delete=models.RESTRICT)
    id_compra = models.ForeignKey(Compra,on_delete=models.RESTRICT)
    id_producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad_producto_servicio = models.IntegerField(verbose_name='Cantidad Productos')
    precio_unitario_servicio = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Precio Unitario')

    class Meta:
        db_table = 'Detalle Servicio'
        verbose_name = 'Detalle Servicio'
        verbose_name_plural = 'Destalle Servicios'

    def __str__(self):
        return f'ID: {self.id_detalle_servicio}, Compra {self.id_compra}, Cliente {self.id_compra.id_usuario.correo_usuario}'

class Detalle_Compra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True,verbose_name='ID')
    id_compra = models.ForeignKey(Compra,on_delete=models.RESTRICT)
    id_producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad_producto_compra = models.IntegerField(verbose_name='Cantidad Productos')
    precio_unitario_compra = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Precio Unitario')

    class Meta:
        db_table = 'Detalle Compra'
        verbose_name = 'Detalle Compra'
        verbose_name_plural = 'Detalles Compras'

    def __str__(self):
        return f'ID: {self.id_detalle_compra}, Compra: {self.id_compra}, Usuario: {self.id_compra.id_usuario.correo_usuario}'
    
class Comprobante_Pago(models.Model):
    id_comprobante = models.AutoField(primary_key=True,verbose_name='ID')
    id_compra = models.ForeignKey(Compra,on_delete=models.RESTRICT)
    fecha_comprobante = models.DateField()
    codigo_comprobante = models.CharField(max_length=20,verbose_name='Codigo De Comprobante')
    estado_comprobante = models.CharField(max_length=2,verbose_name='Estado Comprobante')

    class Meta:
        db_table = 'Comprobante Pago'
        verbose_name = 'Comprobante Pago'
        verbose_name_plural = 'Comprobante Pagos'

    def __str__(self):
        return f'ID: {self.id_comprobante}, Fecha: {self.fecha_comprobante}, Usuario: {self.id_compra.id_usuario.correo_usuario}'

