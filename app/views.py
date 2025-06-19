from django.shortcuts import render,redirect

# Create your views here.

#Funcion Login, Muestra la vista Login.html
def Login(request):
    return render(request,'login.html')

#Funcion Crear_Cuenta, Muestra la vista registro.html
def Crear_Cuenta(request):
    return render(request,'registro.html')