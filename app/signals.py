import requests
import threading
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Usuario, Producto

# **Para Usuario**
@receiver(pre_save, sender=Usuario)
def guardar_imagen_anterior_usuario(sender, instance, **kwargs):
    try:
        instance._imagen_anterior = Usuario.objects.get(pk=instance.pk).imagen_usuario
    except Usuario.DoesNotExist:
        instance._imagen_anterior = None

def subir_imagen_usuario(path, url):
    try:
        with open(path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files, timeout=5)
            response.raise_for_status()
            print('Imagen de usuario subida correctamente al servidor')
    except requests.exceptions.RequestException as e:
        print(f'Error al subir imagen de usuario: {e}')

@receiver(post_save, sender=Usuario)
def enviar_imagen_usuario(sender, instance, created, **kwargs):
    imagen_nueva = instance.imagen_usuario
    imagen_anterior = getattr(instance, '_imagen_anterior', None)

    # Si no hay imagen nueva o no cambió, no hacemos nada
    if not imagen_nueva or imagen_nueva == imagen_anterior:
        return

    ruta_imagen = instance.imagen_usuario.path
    url_servidor = 'http://3.140.248.123/usuario/'  # Cambia esta URL si es necesario

    threading.Thread(target=subir_imagen_usuario, args=(ruta_imagen, url_servidor)).start()


# **Para Producto**
@receiver(pre_save, sender=Producto)
def guardar_imagen_anterior_producto(sender, instance, **kwargs):
    try:
        instance._imagen_anterior = Producto.objects.get(pk=instance.pk).imagen_producto
    except Producto.DoesNotExist:
        instance._imagen_anterior = None

def subir_imagen_producto(path, url):
    try:
        with open(path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files, timeout=5)
            response.raise_for_status()
            print('Imagen de producto subida correctamente al servidor')
    except requests.exceptions.RequestException as e:
        print(f'Error al subir imagen del producto: {e}')

@receiver(post_save, sender=Producto)
def enviar_imagen_producto(sender, instance, created, **kwargs):
    imagen_nueva = instance.imagen_producto
    imagen_anterior = getattr(instance, '_imagen_anterior', None)

    # Si no hay imagen nueva o no cambió, no hacemos nada
    if not imagen_nueva or imagen_nueva == imagen_anterior:
        return

    ruta_imagen = instance.imagen_producto.path
    url_servidor = 'http://3.140.248.123/producto/'  # Cambia esta URL si es necesario

    threading.Thread(target=subir_imagen_producto, args=(ruta_imagen, url_servidor)).start()
