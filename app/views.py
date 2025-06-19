from django.shortcuts import render,redirect

# Create your views here.

"""
Funcion Login, donde se validara la contraseña y correo electronico
para poder iniciar sesion.
"""
def Login(request):
    return render(request,'login.html')