def usuario_context(request):
    contexto = {
        'rol_usuario': 'Director',
        'es_admin': True,
        'nombre_usuario': 'Admin',
    }
    
    if request.user.is_authenticated:
        username = request.user.username
        try:
            from core.models import Usuario
            usuario_db = Usuario.objects.get(username__iexact=username)
            contexto['rol_usuario'] = usuario_db.rol
            contexto['nombre_usuario'] = usuario_db.nombre
            contexto['es_admin'] = usuario_db.rol in ['Director', 'Subdirector']
        except:

            contexto['rol_usuario'] = 'Director'
            contexto['nombre_usuario'] = request.user.username or 'Admin'
            contexto['es_admin'] = True
    
    return contexto