from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.conf import settings
from .models import Permiso
from django.contrib import messages
from django.utils.dateparse import parse_date
from core.validation import parse_decimal_at_least, parse_integer_at_least
import os



TIPOS_COMPROBANTE_PERMITIDOS = [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'application/pdf'
]


def _fechas_en_orden(fecha_inicio, fecha_fin):
    inicio = parse_date(fecha_inicio) if fecha_inicio else None
    fin = parse_date(fecha_fin) if fecha_fin else None
    return inicio is not None and fin is not None and inicio <= fin


def _get_user_info(request):
    """Obtiene rol, user_id e id_profesor. Lee id_profesor directo de la BD."""
    rol = request.session.get('rol')
    user_id = request.session.get('usuario_id')
    id_profesor = None
    
    if rol == 'Profesor' and user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_profesor FROM usuarios WHERE id_usuario = %s", [user_id])
                row = cursor.fetchone()
                if row and row[0] is not None:
                    id_profesor = row[0]
        except Exception as e:
            print(f"DEBUG ERROR al obtener id_profesor: {e}")
    
    return rol, user_id, id_profesor


def _guardar_comprobante(archivo, prof_id, fecha_ini):
    """
    Función auxiliar para guardar el comprobante en el servidor.
    Retorna la ruta relativa a MEDIA_ROOT (sin 'media/' al inicio).
    """
    if not archivo:
        return None
    

    if archivo.content_type not in TIPOS_COMPROBANTE_PERMITIDOS:
        return None
    

    carpeta = os.path.join(settings.MEDIA_ROOT, 'comprobantes')
    os.makedirs(carpeta, exist_ok=True)
    

    safe_filename = "".join(c for c in archivo.name if c.isalnum() or c in ('.', '_', '-'))
    nombre_archivo = f"permiso_{prof_id}_{fecha_ini}_{safe_filename}"
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    

    with open(ruta_completa, 'wb+') as destino:
        for chunk in archivo.chunks():
            destino.write(chunk)
    

    return f'comprobantes/{nombre_archivo}'


def lista(request):
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor' and id_profesor is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id_permiso, p.tipo_permiso, p.fecha_inicio, p.fecha_fin, 
                       p.horas_afectadas, p.estado, p.motivo, pr.nombre as nombre_profesor,
                       p.comprobante
                FROM permisos p
                LEFT JOIN profesores pr ON p.id_profesor = pr.id_profesor
                WHERE p.id_profesor = %s
                ORDER BY p.fecha_inicio DESC
            """, [id_profesor])
            permisos_raw = cursor.fetchall()
            permisos = [
                {
                    'id_permiso': row[0],
                    'tipo_permiso': row[1],
                    'fecha_inicio': row[2],
                    'fecha_fin': row[3],
                    'horas_afectadas': row[4],
                    'estado': row[5],
                    'motivo': row[6],
                    'nombre_profesor': row[7] or f'Profesor #{id_profesor}',
                    'comprobante': row[8]
                }
                for row in permisos_raw
            ]
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id_permiso, p.tipo_permiso, p.fecha_inicio, p.fecha_fin, 
                       p.horas_afectadas, p.estado, p.motivo, pr.nombre as nombre_profesor,
                       p.comprobante
                FROM permisos p
                LEFT JOIN profesores pr ON p.id_profesor = pr.id_profesor
                ORDER BY p.fecha_inicio DESC
            """)
            permisos_raw = cursor.fetchall()
            permisos = [
                {
                    'id_permiso': row[0],
                    'tipo_permiso': row[1],
                    'fecha_inicio': row[2],
                    'fecha_fin': row[3],
                    'horas_afectadas': row[4],
                    'estado': row[5],
                    'motivo': row[6],
                    'nombre_profesor': row[7] or f'Profesor #{row[0]}',
                    'comprobante': row[8]
                }
                for row in permisos_raw
            ]
    
    return render(request, 'permisos/lista.html', {
        'permisos': permisos,
        'rol_usuario': rol,
    })


def crear(request):
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo_permiso', '').strip()
        fecha_ini = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        horas = request.POST.get('horas_afectadas', 0)
        motivo = request.POST.get('motivo', '').strip()

        try:
            horas = parse_decimal_at_least(
                horas or 0, 'Las horas afectadas', maximum=24
            )
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('/permisos/crear/')
        
        if fecha_ini and fecha_fin and not _fechas_en_orden(fecha_ini, fecha_fin):
            messages.error(request, 'Verifica las fechas: el inicio debe ser igual o anterior al fin.')
            return redirect('/permisos/crear/')

        if rol == 'Profesor':
            if not id_profesor:
                messages.error(request, ' Error: Tu usuario no tiene un perfil de profesor vinculado. Contacta al administrador.')
                return redirect('/permisos/crear/')
            prof_id = id_profesor
        else:
            prof_id = request.POST.get('id_profesor')
            if not prof_id:
                messages.error(request, ' Debes seleccionar un profesor.')
                return redirect('/permisos/crear/')
            try:
                prof_id = parse_integer_at_least(
                    prof_id, 'El profesor', minimum=1
                )
            except ValueError as error:
                messages.error(request, str(error))
                return redirect('/permisos/crear/')
        

        if 'comprobante' not in request.FILES:
            messages.error(request, ' Debes subir el comprobante (foto o PDF). Es obligatorio.')
            return redirect('/permisos/crear/')
        
        archivo = request.FILES['comprobante']
        

        if archivo.content_type not in TIPOS_COMPROBANTE_PERMITIDOS:
            messages.error(request, ' El comprobante debe ser una imagen (JPG, PNG) o PDF.')
            return redirect('/permisos/crear/')
        

        comprobante_path = _guardar_comprobante(archivo, prof_id, fecha_ini)
        
        if not comprobante_path:
            messages.error(request, ' Error al guardar el comprobante. Intenta de nuevo.')
            return redirect('/permisos/crear/')
        

        if tipo and fecha_ini and fecha_fin:
            Permiso.objects.create(
                id_profesor=prof_id,
                tipo_permiso=tipo,
                fecha_inicio=fecha_ini,
                fecha_fin=fecha_fin,
                horas_afectadas=horas,
                motivo=motivo,
                estado='pendiente',
                id_usuario_registro=user_id,
                comprobante=comprobante_path
            )
            messages.success(request, ' Permiso creado exitosamente')
            return redirect('/permisos/')
        else:
            messages.error(request, ' Completa todos los campos obligatorios.')
    
    profesores = []
    if rol != 'Profesor':
        from core.models import Profesor
        profesores = Profesor.objects.filter(estado=True).order_by('nombre')
    
    return render(request, 'permisos/form.html', {
        'accion': 'Crear',
        'rol_usuario': rol,
        'profesores': profesores,
        'es_profesor': rol == 'Profesor',
    })


def editar(request, id_permiso):
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor':
        messages.error(request, ' No tienes permisos para editar.')
        return redirect('/permisos/')
    
    permiso = get_object_or_404(Permiso, id_permiso=id_permiso)
    
    if request.method == 'POST':
        permiso.tipo_permiso = request.POST.get('tipo_permiso', '').strip()
        permiso.fecha_inicio = request.POST.get('fecha_inicio')
        permiso.fecha_fin = request.POST.get('fecha_fin')
        try:
            permiso.horas_afectadas = parse_decimal_at_least(
                request.POST.get('horas_afectadas') or 0,
                'Las horas afectadas',
                maximum=24,
            )
        except ValueError as error:
            messages.error(request, str(error))
            return redirect(f'/permisos/editar/{id_permiso}/')
        permiso.motivo = request.POST.get('motivo', '').strip()
        permiso.estado = request.POST.get('estado', 'pendiente')
        
        if permiso.fecha_inicio and permiso.fecha_fin and not _fechas_en_orden(
            permiso.fecha_inicio, permiso.fecha_fin
        ):
            messages.error(request, 'Verifica las fechas: el inicio debe ser igual o anterior al fin.')
            return redirect(f'/permisos/editar/{id_permiso}/')

        if 'comprobante' in request.FILES:
            archivo = request.FILES['comprobante']
            

            if archivo.content_type not in TIPOS_COMPROBANTE_PERMITIDOS:
                messages.error(request, ' El comprobante debe ser una imagen (JPG, PNG) o PDF.')
                return redirect(f'/permisos/editar/{id_permiso}/')
            

            nuevo_path = _guardar_comprobante(archivo, permiso.id_profesor, permiso.fecha_inicio)
            
            if nuevo_path:

                if permiso.comprobante:
                    ruta_anterior = os.path.join(settings.MEDIA_ROOT, permiso.comprobante)
                    if os.path.exists(ruta_anterior):
                        os.remove(ruta_anterior)
                
                permiso.comprobante = nuevo_path
            else:
                messages.error(request, ' Error al guardar el nuevo comprobante.')
                return redirect(f'/permisos/editar/{id_permiso}/')
        

        if permiso.tipo_permiso and permiso.fecha_inicio and permiso.fecha_fin:
            permiso.save()
            messages.success(request, ' Permiso actualizado')
            return redirect('/permisos/')
        else:
            messages.error(request, ' Completa todos los campos obligatorios.')
    
    from core.models import Profesor
    profesores = Profesor.objects.filter(estado=True).order_by('nombre')
    
    return render(request, 'permisos/form.html', {
        'permiso': permiso,
        'accion': 'Editar',
        'rol_usuario': rol,
        'profesores': profesores,
    })


def eliminar(request, id_permiso):
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor':
        messages.error(request, ' No tienes permisos para eliminar.')
        return redirect('/permisos/')
    
    permiso = get_object_or_404(Permiso, id_permiso=id_permiso)
    

    if permiso.comprobante:
        ruta_archivo = os.path.join(settings.MEDIA_ROOT, permiso.comprobante)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
    
    permiso.delete()
    messages.success(request, ' Permiso eliminado')
    return redirect('/permisos/')