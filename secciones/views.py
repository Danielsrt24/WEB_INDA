from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
import django.db.models as models
from core.permissions import requiere_director
from .models import Seccion, Estudiante






def lista_secciones(request):
    """Muestra la lista de todas las secciones."""
    secciones = Seccion.objects.filter(estado=True).annotate(
        estudiantes_count=Count('estudiantes', filter=models.Q(estudiantes__estado=True))
    ).order_by('nombre')
    return render(request, 'secciones/lista.html', {'secciones': secciones})


def crear_seccion(request):
    """Crea una nueva sección."""
    if request.method == 'POST':
        Seccion.objects.create(
            nombre=request.POST.get('nombre', '').strip(),
            nivel=request.POST.get('nivel', '').strip(),
            letra=request.POST.get('letra', '').strip(),
            estado=True
        )
        messages.success(request, ' Sección creada exitosamente')
        return redirect('secciones:lista')
    
    return render(request, 'secciones/form.html', {'accion': 'Crear'})


def editar_seccion(request, pk):
    """Edita una sección existente."""
    seccion = get_object_or_404(Seccion, pk=pk)
    
    if request.method == 'POST':
        seccion.nombre = request.POST.get('nombre', '').strip()
        seccion.nivel = request.POST.get('nivel', '').strip()
        seccion.letra = request.POST.get('letra', '').strip()
        seccion.save()
        
        messages.success(request, ' Sección actualizada exitosamente')
        return redirect('secciones:lista')
    
    return render(request, 'secciones/form.html', {
        'seccion': seccion,
        'accion': 'Editar'
    })


def eliminar_seccion(request, pk):
    """Elimina (desactiva) una sección."""
    seccion = get_object_or_404(Seccion, pk=pk)
    seccion.estado = False
    seccion.save()
    messages.success(request, ' Sección eliminada exitosamente')
    return redirect('secciones:lista')






def lista_estudiantes(request, seccion_id):
    """Muestra la lista de estudiantes de una sección específica."""
    seccion = get_object_or_404(Seccion, pk=seccion_id)
    estudiantes = Estudiante.objects.filter(id_seccion=seccion, estado=True).order_by('apellido', 'nombre')
    
    return render(request, 'secciones/estudiantes_lista.html', {
        'seccion': seccion,
        'estudiantes': estudiantes
    })


def crear_estudiante(request, seccion_id):
    """Crea un nuevo estudiante en una sección."""
    seccion = get_object_or_404(Seccion, pk=seccion_id)
    
    if request.method == 'POST':
        Estudiante.objects.create(
            id_seccion=seccion,
            nombre=request.POST.get('nombre', '').strip(),
            apellido=request.POST.get('apellido', '').strip(),
            cedula=request.POST.get('cedula', '').strip(),
            fecha_nacimiento=request.POST.get('fecha_nacimiento', None) or None,
            sexo=request.POST.get('sexo', '').strip(),
            estado=True
        )
        messages.success(request, ' Estudiante creado exitosamente')
        return redirect('secciones:estudiantes', seccion_id=seccion.pk)
    
    return render(request, 'secciones/estudiante_form.html', {
        'seccion': seccion,
        'accion': 'Crear'
    })


def editar_estudiante(request, pk):
    """Edita un estudiante existente."""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    seccion = estudiante.id_seccion
    
    if request.method == 'POST':
        estudiante.nombre = request.POST.get('nombre', '').strip()
        estudiante.apellido = request.POST.get('apellido', '').strip()
        estudiante.cedula = request.POST.get('cedula', '').strip()
        estudiante.fecha_nacimiento = request.POST.get('fecha_nacimiento', None) or None
        estudiante.sexo = request.POST.get('sexo', '').strip()
        estudiante.save()
        
        messages.success(request, ' Estudiante actualizado exitosamente')
        return redirect('secciones:estudiantes', seccion_id=seccion.pk)
    
    return render(request, 'secciones/estudiante_form.html', {
        'estudiante': estudiante,
        'seccion': seccion,
        'accion': 'Editar'
    })


def eliminar_estudiante(request, pk):
    """Elimina (desactiva) un estudiante."""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    seccion = estudiante.id_seccion
    
    estudiante.estado = False
    estudiante.save()
    
    messages.success(request, ' Estudiante eliminado exitosamente')
    return redirect('secciones:estudiantes', seccion_id=seccion.pk)