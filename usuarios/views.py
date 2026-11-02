from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from .models import Usuario
import bcrypt


def lista_usuarios(request):
    """Muestra la lista de todos los usuarios del sistema."""
    rol = request.session.get('rol')
    
    if not rol or rol not in ['Director', 'Subdirector']:
        messages.error(request, ' No tienes permisos para ver esta página')
        return redirect('/dashboard/')
    
    usuarios = Usuario.objects.filter(estado=1).order_by('nombre')
    
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios,
        'rol_usuario': rol,
    })


def crear_usuario(request):
    """Crea un nuevo usuario y lo vincula automáticamente si es profesor."""
    rol_sesion = request.session.get('rol')
    
    if not rol_sesion or rol_sesion not in ['Director', 'Subdirector']:
        messages.error(request, ' No tienes permisos')
        return redirect('/dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        rol_usuario = request.POST.get('rol', '').strip()
        
        if not username or not password or not nombre or not rol_usuario:
            messages.error(request, ' Completa todos los campos obligatorios')
            return redirect('/usuarios/crear/')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f' El usuario "{username}" ya existe')
            return redirect('/usuarios/crear/')
        

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        

        nuevo_usuario = Usuario.objects.create(
            username=username,
            password_hash=password_hash,
            nombre=nombre,
            rol=rol_usuario,
            email=email,
            estado=1,
            id_profesor=None
        )
        

        if rol_usuario == 'Profesor':
            from core.models import Profesor
            
            nuevo_profesor = Profesor.objects.create(
                nombre=nombre,
                email=email,
                estado=1,
                id_usuario=nuevo_usuario.id_usuario
            )
            
            nuevo_usuario.id_profesor = nuevo_profesor.id_profesor
            nuevo_usuario.save()
            
            messages.success(request, f' Profesor "{nombre}" creado y vinculado exitosamente')
        else:
            messages.success(request, f' Usuario {rol_usuario} "{username}" creado exitosamente')
        
        return redirect('/usuarios/')
    
    return render(request, 'usuarios/form.html', {
        'accion': 'Crear',
        'rol_usuario': rol_sesion,
    })

def editar_usuario(request, user_id):
    """Edita un usuario existente."""
    rol = request.session.get('rol')
    
    if not rol or rol not in ['Director', 'Subdirector']:
        messages.error(request, ' No tienes permisos')
        return redirect('/dashboard/')
    
    usuario = get_object_or_404(Usuario, pk=user_id)
    
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        estado = request.POST.get('estado')
        
        usuario.nombre = nombre
        usuario.email = email
        usuario.estado = 1 if estado else 0
        

        if password:
            usuario.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        usuario.save()
        
        messages.success(request, ' Usuario actualizado exitosamente')
        return redirect('/usuarios/')
    
    return render(request, 'usuarios/form.html', {
        'usuario': usuario,
        'accion': 'Editar',
        'rol_usuario': rol,
    })


def eliminar_usuario(request, user_id):
    """Elimina (desactiva) un usuario."""
    rol = request.session.get('rol')
    
    if not rol or rol != 'Director':
        messages.error(request, ' Solo el Director puede eliminar usuarios')
        return redirect('/usuarios/')
    
    usuario = get_object_or_404(Usuario, pk=user_id)
    

    usuario_actual_id = request.session.get('usuario_id')
    if usuario.id_usuario == usuario_actual_id:
        messages.error(request, ' No puedes eliminarte a ti mismo')
        return redirect('/usuarios/')
    
    usuario.estado = 0
    usuario.save()
    
    messages.success(request, ' Usuario eliminado exitosamente')
    return redirect('/usuarios/')