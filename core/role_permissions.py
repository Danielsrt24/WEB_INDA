"""
Matriz de Permisos REAL del Sistema INDA
Basada en la tabla oficial de accesos por rol.
"""

MATRIZ_PERMISOS = {
    'Director': {
        'permisos':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'distribucion': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'horarios':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'materias':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'secciones':    {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'notas':        {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
    },
    'Subdirector': {
        'permisos':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'distribucion': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'horarios':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'materias':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'secciones':    {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'notas':        {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
    },
    'Secretaria': {
        'permisos':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'distribucion': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'horarios':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'materias':     {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'secciones':    {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'notas':        {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    },
'Profesor': {
    'permisos':     {'ver': True, 'crear': True, 'editar': False, 'eliminar': False},
    'distribucion': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    'horarios':     {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    'materias':     {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    'secciones':    {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    'notas':        {'ver': True, 'crear': True, 'editar': True, 'eliminar': False},
},
}


def puede(rol, modulo, accion):
    """
    Verifica si un rol tiene permiso para una acción en un módulo.
    Uso: puede('Director', 'materias', 'crear') -> True/False
    """
    if not rol:
        return False
    permisos_rol = MATRIZ_PERMISOS.get(rol, {})
    permisos_modulo = permisos_rol.get(modulo, {})
    return permisos_modulo.get(accion, False)


def es_admin(rol):
    """Retorna True si el rol es Director o Subdirector."""
    return rol in ['Director', 'Subdirector']