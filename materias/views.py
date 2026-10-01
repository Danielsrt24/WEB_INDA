from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Materia
from core.permissions import login_required_custom, puede_editar, requiere_admin

@login_required_custom
def lista_materias(request):
    materias = Materia.objects.filter(estado=True)
    return render(request, 'materias/lista.html', {
        'materias': materias,
        'puede_editar': puede_editar(request)
    })

@requiere_admin
def crear_materia(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        creditos = request.POST.get('creditos', 0)
        
        if Materia.objects.filter(codigo=codigo).exists():
            messages.error(request, 'El código ya existe')
            return redirect('materias:crear')
        
        Materia.objects.create(codigo=codigo, nombre=nombre, creditos=int(creditos))
        messages.success(request, 'Materia creada')
        return redirect('materias:lista')
    return render(request, 'materias/form.html', {'accion': 'Crear'})

@requiere_admin
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        materia.codigo = request.POST.get('codigo')
        materia.nombre = request.POST.get('nombre')
        materia.creditos = int(request.POST.get('creditos', 0))
        materia.save()
        messages.success(request, 'Materia actualizada')
        return redirect('materias:lista')
    return render(request, 'materias/form.html', {'materia': materia, 'accion': 'Editar'})

@requiere_admin
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    materia.estado = False
    materia.save()
    messages.success(request, 'Materia eliminada')
    return redirect('materias:lista')