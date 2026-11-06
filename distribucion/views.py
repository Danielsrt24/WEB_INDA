from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.permissions import requiere_director

from .models import Distribucion
from core.models import Profesor
from materias.models import Materia
from secciones.models import Seccion
from core.validation import parse_integer_at_least


@requiere_director
def lista_distribucion(request):
    """Muestra la lista de todas las distribuciones activas."""
    distribuciones = Distribucion.objects.filter(estado=True)
    

    profesores = Profesor.objects.filter(estado=True)
    materias = Materia.objects.filter(estado=True)
    secciones = Seccion.objects.filter(estado=True)
    
    return render(request, 'distribucion/lista.html', {
        'distribuciones': distribuciones,
        'profesores': profesores,
        'materias': materias,
        'secciones': secciones
    })


@requiere_director
def crear_distribucion(request):
    """Crea una nueva distribución."""
    if request.method == 'POST':
        try:
            id_profesor = parse_integer_at_least(
                request.POST.get('id_profesor'), 'El profesor', minimum=1
            )
            id_materia = parse_integer_at_least(
                request.POST.get('id_materia'), 'La materia', minimum=1
            )
            id_seccion = parse_integer_at_least(
                request.POST.get('id_seccion'), 'La sección', minimum=1
            )
            horas_semanales = parse_integer_at_least(
                request.POST.get('horas_semanales', 0), 'Las horas semanales'
            )
            nueva_dist = Distribucion(
                id_profesor_id=id_profesor,
                id_materia_id=id_materia,
                id_seccion_id=id_seccion,
                horas_semanales=horas_semanales,
                estado=True
            )
            nueva_dist.save()
            messages.success(request, 'Distribución creada exitosamente')
            return redirect('distribucion:lista')
        except Exception as e:
            messages.error(request, f'Error al crear la distribución: {str(e)}')
    

    profesores = Profesor.objects.filter(estado=True)
    materias = Materia.objects.filter(estado=True)
    secciones = Seccion.objects.filter(estado=True)
    
    return render(request, 'distribucion/form.html', {
        'profesores': profesores,
        'materias': materias,
        'secciones': secciones,
        'accion': 'Crear'
    })


@requiere_director
def editar_distribucion(request, pk):
    """Edita una distribución existente."""
    distribucion = get_object_or_404(Distribucion, pk=pk)

    if request.method == 'POST':
        try:
            distribucion.id_profesor_id = parse_integer_at_least(
                request.POST.get('id_profesor'), 'El profesor', minimum=1
            )
            distribucion.id_materia_id = parse_integer_at_least(
                request.POST.get('id_materia'), 'La materia', minimum=1
            )
            distribucion.id_seccion_id = parse_integer_at_least(
                request.POST.get('id_seccion'), 'La sección', minimum=1
            )
            distribucion.horas_semanales = parse_integer_at_least(
                request.POST.get('horas_semanales', 0), 'Las horas semanales'
            )
            
            distribucion.save()
            messages.success(request, 'Distribución actualizada exitosamente')
            return redirect('distribucion:lista')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')


    profesores = Profesor.objects.filter(estado=True)
    materias = Materia.objects.filter(estado=True)
    secciones = Seccion.objects.filter(estado=True)

    return render(request, 'distribucion/form.html', {
        'distribucion': distribucion,
        'profesores': profesores,
        'materias': materias,
        'secciones': secciones,
        'accion': 'Editar'
    })


@requiere_director
def eliminar_distribucion(request, pk):
    """Elimina (desactiva) una distribución."""
    distribucion = get_object_or_404(Distribucion, pk=pk)
    distribucion.estado = False
    distribucion.save()
    messages.success(request, 'Distribución desactivada exitosamente')
    return redirect('distribucion:lista')