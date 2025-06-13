from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Servicio)
admin.site.register(Categoria_Servicio)
admin.site.register(Compra)
admin.site.register(Comprobante_Pago)
admin.site.register(Detalle_Servicio)
admin.site.register(Detalle_Compra)
admin.site.register(Producto)
admin.site.register(Categoria)