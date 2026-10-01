from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Permiso
from core.permissions import login_required_custom, puede_editar, requiere_admin

@login_required_custom
def lista_permisos(request):
    permisos = Permiso.objects.all().order_by('-fecha_registro')
    return render(request, 'permisos/lista.html', {
        'permisos': permisos,
        'puede_editar': puede_editar(request)
    })

@requiere_admin
def crear_permiso(request):
    if request.method == 'POST':
        try:
            Permiso.objects.create(
                id_profesor=int(request.POST.get('id_profesor')),
                tipo_permiso=request.POST.get('tipo_permiso'),
                fecha_inicio=request.POST.get('fecha_inicio'),
                fecha_fin=request.POST.get('fecha_fin'),
                motivo=request.POST.get('motivo', ''),
                horas_afectadas=float(request.POST.get('horas_afectadas') or 0),
                estado='pendiente',
                id_usuario_registro=request.session.get('usuario_id')
            )
            messages.success(request, 'Permiso creado')
            return redirect('permisos:lista')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'permisos/form.html', {'accion': 'Crear'})

@requiere_admin
def editar_permiso(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == 'POST':
        permiso.tipo_permiso = request.POST.get('tipo_permiso')
        permiso.fecha_inicio = request.POST.get('fecha_inicio')
        permiso.fecha_fin = request.POST.get('fecha_fin')
        permiso.motivo = request.POST.get('motivo', '')
        permiso.save()
        messages.success(request, 'Permiso actualizado')
        return redirect('permisos:lista')
    return render(request, 'permisos/form.html', {'permiso': permiso, 'accion': 'Editar'})

@requiere_admin
def eliminar_permiso(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    permiso.estado = 'cancelado'
    permiso.save()
    messages.success(request, 'Permiso cancelado')
    return redirect('permisos:lista')