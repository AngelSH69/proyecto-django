from django.shortcuts import render, HttpResponse

# Vistas de la aplicación 'inicio'.


def principal(request):
    return render(request,"inicio/principal.html")

def contacto(request):
    return render(request, "inicio/contacto.html")

def nombre(request):
    contenido="<h1> Angel Gabriel Suarez Huerta</h1>"
    return HttpResponse(contenido)

def formulario(request):
    return render(request, "inicio/formulario.html")  

def ejemplo(request):
    return render(request,"inicio/ejemplo.html")