from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Usuario
from core.permissions import requiere_director

@requiere_director
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@requiere_director
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        rol = request.POST.get('rol')
        email = request.POST.get('email')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('usuarios:crear')

        Usuario.objects.create(
            username=username,
            password_hash=password,
            nombre=nombre,
            rol=rol,
            email=email,
            estado=True
        )
        messages.success(request, f'Usuario {username} creado')
        return redirect('usuarios:lista')

    return render(request, 'usuarios/form.html', {'accion': 'Crear'})

@requiere_director
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.rol = request.POST.get('rol')
        usuario.email = request.POST.get('email')
        nueva_pass = request.POST.get('password')
        if nueva_pass:
            usuario.password_hash = nueva_pass
        usuario.save()
        messages.success(request, 'Usuario actualizado')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/form.html', {'usuario': usuario, 'accion': 'Editar'})

@requiere_director
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.estado = False
    usuario.save()
    messages.success(request, 'Usuario desactivado')
    return redirect('usuarios:lista')