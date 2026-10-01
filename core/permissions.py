from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required_custom(view_func):
    """Verifica que el usuario esté logueado"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('core:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def solo_ver(request):
    """Solo Profesor puede ver (no editar/crear/eliminar)"""
    rol = request.session.get('rol')
    return rol == 'Profesor'

def puede_editar(request):
    """Director, Subdirector y Secretaria pueden editar"""
    rol = request.session.get('rol')
    return rol in ['Director', 'Subdirector', 'Secretaria']

def requiere_admin(view_func):
    """Solo Director, Subdirector y Secretaria pueden acceder"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('core:login')
        if not puede_editar(request):
            messages.error(request, 'No tienes permisos para acceder a esta sección')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def requiere_director(view_func):
    """Solo Director"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('core:login')
        if request.session.get('rol') != 'Director':
            messages.error(request, 'Solo el Director puede acceder')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper