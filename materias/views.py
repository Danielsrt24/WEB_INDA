from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Materia
from core.permissions import login_required_custom, puede_editar, requiere_admin
from core.validation import parse_integer_at_least

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
        try:
            creditos = parse_integer_at_least(creditos, 'Los créditos')
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('materias:crear')
        
        if Materia.objects.filter(codigo=codigo).exists():
            messages.error(request, 'Ese código de materia ya está en uso. Ingresa uno diferente.')
            return redirect('materias:crear')
        
        try:
            Materia.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
        except IntegrityError:
            messages.error(request, 'Ese código de materia ya está en uso. Ingresa uno diferente.')
            return redirect('materias:crear')
        messages.success(request, 'Materia creada')
        return redirect('materias:lista')
    return render(request, 'materias/form.html', {'accion': 'Crear'})

@requiere_admin
def editar_materia(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        try:
            creditos = parse_integer_at_least(
                request.POST.get('creditos', 0), 'Los créditos'
            )
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('materias:editar', pk=pk)
        codigo = request.POST.get('codigo')
        if Materia.objects.filter(codigo=codigo).exclude(pk=pk).exists():
            messages.error(request, 'Ese código de materia ya está en uso. Ingresa uno diferente.')
            return redirect('materias:editar', pk=pk)
        materia.codigo = codigo
        materia.nombre = request.POST.get('nombre')
        materia.creditos = creditos
        try:
            materia.save()
        except IntegrityError:
            messages.error(request, 'Ese código de materia ya está en uso. Ingresa uno diferente.')
            return redirect('materias:editar', pk=pk)
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