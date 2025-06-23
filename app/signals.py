from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Usuario
import requests

# Guardamos temporalmente la imagen anterior
@receiver(pre_save, sender=Usuario)
def guardar_imagen_anterior(sender, instance, **kwargs):
    try:
        instance._imagen_anterior = Usuario.objects.get(pk=instance.pk).imagen_usuario
    except Usuario.DoesNotExist:
        instance._imagen_anterior = None

@receiver(post_save, sender=Usuario)
def enviar_imagen_al_servidor(sender, instance, created, **kwargs):
    imagen_nueva = instance.imagen_usuario
    imagen_anterior = getattr(instance, '_imagen_anterior', None)

    # Si no hay imagen nueva o no cambió, no hacemos nada
    if not imagen_nueva or imagen_nueva == imagen_anterior:
        return

    try:
        ruta_imagen = instance.imagen_usuario.path
        url_servidor = 'http://18.223.98.41/usuario/'

        with open(ruta_imagen, 'rb') as file:
            files = {'file': file}
            response = requests.post(url_servidor, files=files)
        response.raise_for_status()
        print('Imagen transferida con éxito al servidor EC2')
    except requests.exceptions.RequestException as e:
        print(f'Error al transferir la imagen al servidor EC2: {e}')
