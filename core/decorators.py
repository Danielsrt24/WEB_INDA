from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from core.role_permissions import puede


def require_permission(modulo, accion):
    """
    Decorador para proteger vistas según la matriz de permisos.
    Si el usuario no tiene permisos, muestra alerta y redirige al dashboard.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta sección.')
                return redirect('/login/')
            

            rol = None
            try:
                from core.models import Usuario
                usuario_db = Usuario.objects.get(username=request.user.username)
                rol = usuario_db.rol
            except Exception as e:
                print(f"Error obteniendo rol en decorator: {e}")
                rol = 'Director'
            

            if not puede(rol, modulo, accion):
                messages.error(
                    request, 
                    f' No tienes permisos para {accion} en el módulo de {modulo}. '
                    f'Tu rol actual es: {rol}'
                )
                return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_rol(*roles_permitidos):
    """
    Decorador para permitir solo ciertos roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta sección.')
                return redirect('/login/')
            
            rol = None
            try:
                from core.models import Usuario
                usuario_db = Usuario.objects.get(username=request.user.username)
                rol = usuario_db.rol
            except Exception:
                rol = 'Director'
            
            if rol not in roles_permitidos:
                messages.error(
                    request,
                    f' Acceso restringido. Esta sección solo está disponible para: {", ".join(roles_permitidos)}. '
                    f'Tu rol actual es: {rol}'
                )
                return redirect('/dashboard/')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator