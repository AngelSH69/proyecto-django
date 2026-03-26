import datetime

from django.shortcuts import render
from .models import Alumnos, ComentarioContacto, Archivos
from .forms import ComentarioContactoForm,FormArchivos
from django.shortcuts import get_object_or_404
import datetime
from django.contrib import messages

def registros(request):
    alumnos = Alumnos.objects.all()
    return render(request, 'registros/principal.html', {'8A': alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registros/contacto.html')
    form = ComentarioContactoForm()
    return render(request, 'registros/contacto.html', {'form': form})

def contacto(request):
    return render(request, 'registros/contacto.html')

def comentarios(request):
    comentario = ComentarioContacto.objects.all()
    return render(request, 'registros/contactoMensaje.html', {'Comentario': comentario})

def eliminarComentarioContacto(request, id):
    confirmacion = 'registros/confirmarEliminacion.html'
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render (request,'registros/contactoMensaje.html',{'Comentario':comentarios})
    return render(request, confirmacion)

def consultarComentarioIndividual(request, id):
    comentarrio=ComentarioContacto.objects.get(id=id)
    #get permite establecer una condición para obtener un registro específico, en este caso el id del comentario
    return render(request,'registros/formEditarComentario.html',
                  {'comentario':comentarrio})
        
def editarComentarioContacto(request, id):
        comentario = get_object_or_404(ComentarioContacto, id=id)
        form = ComentarioContactoForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            comentarios=ComentarioContacto.objects.all()
            return render(request, 'registros/contactoMensaje.html',
                   {'Comentario': comentarios})
        return render(request, 'registros/formEditarComentario.html',
                   {'comentario': comentarios})

def consultar1(request):
    #filter nos retorna un conjunto de registros que cumplen con la condición dada
    #En este caso, se están filtrando los alumnos que pertenecen a la carrera de 'TI'
    alumnos = Alumnos.objects.filter(carrera='TI')
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar2(request):
    #filter nos retorna un conjunto de registros que cumplen con la condición dada
    #En este caso, se están filtrando los alumnos que pertenecen a la carrera de 'TI' y turno
    alumnos = Alumnos.objects.filter(carrera='TI').filter(turno='Matutino')
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar3(request):
    #filter nos retorna un conjunto de registros que cumplen con la condición dada
    #Puedes utilizar filter con only para traer los alumnos de Ti pero solo los nombres
    #EJEMPLO :"alumnos = Alumnos.objects.filter(carrera='TI').only('nombre')"
    alumnos = Alumnos.objects.all().only('matricula', 'nombre', 'carrera', 'turno','imagen')
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar4(request):
    #El __contains es un filtro que se utiliza para buscar registros que contengan una cadena específica en un campo de texto. En este caso, se están filtrando los alumnos cuyo turno contiene la palabra 'Vesp', lo que podría incluir turnos como 'Vespertino' o 'Vespertina'.
    alumnos = Alumnos.objects.filter(turno__contains='Vesp')
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar5(request):
    #El __in es un filtro que se utiliza para buscar registros que coincidan con cualquier valor de una lista específica. En este caso, se están filtrando los alumnos cuyo nombre está en la lista ['Juan', 'Ana'].
    alumnos = Alumnos.objects.filter(nombre__in=['Juan', 'Ana'])
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar6(request):
    #El __range es un filtro que se utiliza para buscar registros que tengan un valor dentro de un rango específico. En este caso, se están filtrando los alumnos cuya fecha de creación (created) está entre el 2 de marzo de 2026 y el 30 de junio de 2026.
    fechaInicio = datetime.date(2026, 3, 2)
    fechaFin = datetime.date(2026, 6, 30)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def consultar7(request):
    #El __contains es un filtro que se utiliza para buscar registros que contengan una cadena específica en un campo de texto. En este caso, se están filtrando los alumnos cuyo comentario relacionado (comentario__coment) contiene la palabra 'No inscrito'.
    #Tabla/campo/relacion
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request, 'registros/consultas.html', {'8A': alumnos})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion= descripcion, archivo= archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
                messages.error(request,"Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})
    
def subirArchivo(request):
    return render(request, 'registros/archivos.html')

def consultasSQL(request):
    alumnos=Alumnos.objects.raw ('SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')

    return render(request, 'registros/consultas.html', {'8A': alumnos})

def seguridad(request, nombre=None):
    nombre = request.GET.get('nombre')
    return render(request, 'inicio/seguridad.html', {'nombre': nombre})
