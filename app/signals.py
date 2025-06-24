from .models import Usuario
import threading
import requests
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Guardamos temporalmente la imagen anterior
@receiver(pre_save, sender=Usuario)
def guardar_imagen_anterior(sender, instance, **kwargs):
    try:
        instance._imagen_anterior = Usuario.objects.get(pk=instance.pk).imagen_usuario
    except Usuario.DoesNotExist:
        instance._imagen_anterior = None

def subir_imagen_a_ec2(path, url):
    try:
        with open(path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files, timeout=5)
            response.raise_for_status()
            print('Imagen transferida con éxito al servidor EC2')
    except requests.exceptions.RequestException as e:
        print(f'Error al transferir la imagen al servidor EC2: {e}')

@receiver(post_save, sender=Usuario)
def enviar_imagen_al_servidor(sender, instance, created, **kwargs):
    imagen_nueva = instance.imagen_usuario
    imagen_anterior = getattr(instance, '_imagen_anterior', None)

    if not imagen_nueva or imagen_nueva == imagen_anterior:
        return

    ruta_imagen = instance.imagen_usuario.path
    url_servidor = 'http://3.140.248.123/usuario/'

    # Ejecutar en segundo plano para no bloquear Django
    threading.Thread(target=subir_imagen_a_ec2, args=(ruta_imagen, url_servidor)).start()
