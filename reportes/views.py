from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from secciones.models import Seccion, Estudiante
from notas.models import Nota
from permisos.models import Permiso
from distribucion.models import Distribucion
from core.models import Profesor


def _verificar_acceso_reportes(request):
    """Función auxiliar para validar que solo Director, Subdirector o Secretaria entren."""
    rol = request.session.get('rol')
    roles_permitidos = ['Director', 'Subdirector', 'Secretaria']
    
    if not rol or rol not in roles_permitidos:
        messages.error(request, ' No tienes permisos para acceder al módulo de reportes.')
        return None
    return rol


def menu_reportes(request):
    rol = _verificar_acceso_reportes(request)
    if not rol:
        return redirect('/dashboard/')
    
    return render(request, 'reportes/menu.html', {'rol_usuario': rol})


def reporte_notas(request):
    rol = _verificar_acceso_reportes(request)
    if not rol:
        return redirect('/dashboard/')
    
    notas_raw = Nota.objects.filter(estado=True).order_by(
        'id_distribucion', 'carnet_estudiante', 'tipo_evaluacion'
    )
    
    dist_ids = list(set(nota.id_distribucion for nota in notas_raw))
    distribuciones = Distribucion.objects.filter(id_distribucion__in=dist_ids).select_related(
        'id_seccion', 'id_materia', 'id_profesor'
    )
    
    dist_map = {d.id_distribucion: d for d in distribuciones}
    
    notas_detalle = []
    for nota in notas_raw:
        dist = dist_map.get(nota.id_distribucion)
        notas_detalle.append({
            'nota': nota,
            'seccion_nombre': dist.id_seccion.nombre if dist and dist.id_seccion else 'N/A',
            'seccion_letra': dist.id_seccion.letra if dist and dist.id_seccion else '',
            'materia_nombre': dist.id_materia.nombre if dist and dist.id_materia else 'N/A',
        })
    
    return render(request, 'reportes/notas_detalle.html', {
        'notas_detalle': notas_detalle,
        'rol_usuario': rol,
        'titulo': 'Reporte Detallado de Calificaciones'
    })


def reporte_permisos(request):
    rol = _verificar_acceso_reportes(request)
    if not rol:
        return redirect('/dashboard/')
    
    permisos_raw = Permiso.objects.all().order_by('-fecha_registro')
    prof_ids = list(set(p.id_profesor for p in permisos_raw if p.id_profesor))
    
    profesores = Profesor.objects.filter(id_profesor__in=prof_ids)
    prof_map = {p.id_profesor: p.nombre for p in profesores}
    
    permisos_detalle = []
    for permiso in permisos_raw:
        nombre_profesor = prof_map.get(permiso.id_profesor, f"Profesor #{permiso.id_profesor}")
        permisos_detalle.append({
            'permiso': permiso,
            'nombre_profesor': nombre_profesor
        })
    
    return render(request, 'reportes/permisos_detalle.html', {
        'permisos': permisos_detalle,
        'rol_usuario': rol,
        'titulo': 'Reporte Detallado de Permisos'
    })


def reporte_estudiantes(request):
    rol = _verificar_acceso_reportes(request)
    if not rol:
        return redirect('/dashboard/')
    
    estudiantes = Estudiante.objects.filter(estado=True).select_related(
        'id_seccion'
    ).order_by(
        'id_seccion__nombre', 'id_seccion__letra', 'apellido', 'nombre'
    )
    
    return render(request, 'reportes/estudiantes_detalle.html', {
        'estudiantes': estudiantes,
        'rol_usuario': rol,
        'titulo': 'Listado General de Estudiantes por Sección'
    })