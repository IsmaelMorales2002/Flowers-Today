from django.shortcuts import render,redirect

# Create your views here.

#Funcion Login, Muestra la vista Login.html
def Vista_Login(request):
    return render(request,'login.html')

#Funcion Crear_Cuenta, Muestra la vista registro.html
def Vista_Crear_Cuenta(request):
    return render(request,'registro.html')