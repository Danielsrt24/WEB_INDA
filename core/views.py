import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

def home(request):
    """Redirige al dashboard si está logueado, si no, al login"""
    if request.session.get('usuario_id'):
        return redirect('core:dashboard')
    return redirect('core:login')

def login_view(request):
    """Maneja el inicio de sesión con verificación bcrypt"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=username, estado=True)
            
            if bcrypt.checkpw(
                password.encode('utf-8'), 
                usuario.password_hash.encode('utf-8')
            ):
                request.session['usuario_id'] = usuario.id_usuario
                request.session['username'] = usuario.username
                request.session['nombre'] = usuario.nombre
                request.session['rol'] = usuario.rol
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
        except Exception as e:
            messages.error(request, f'Error de sistema: {str(e)}')
            
    return render(request, 'core/login.html')

def dashboard(request):
    """Muestra el panel principal"""
    if not request.session.get('usuario_id'):
        return redirect('core:login')
    
    context = {
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
    }
    return render(request, 'core/dashboard.html', context)

def logout_view(request):
    """Cierra la sesión y redirige al login"""
    request.session.flush()
    return redirect('core:login')