import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Nota
from distribucion.models import Distribucion
from secciones.models import Seccion
from materias.models import Materia
from core.validation import parse_decimal_at_least, parse_integer_at_least


def _get_user_info(request):
    """Obtiene rol, user_id e id_profesor desde la SESIÓN."""
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
        except Exception:
            pass
    return rol, user_id, id_profesor


def _get_distribuciones_profesor(id_profesor):
    """Obtiene los IDs de distribución asignados a un profesor."""
    if not id_profesor:
        return []
    dists = Distribucion.objects.filter(id_profesor=id_profesor, estado=True)
    return [d.id_distribucion for d in dists]


def menu_notas(request):
    """Muestra las secciones disponibles para gestionar notas."""
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor':
        dist_ids = _get_distribuciones_profesor(id_profesor)
        secciones = Seccion.objects.filter(
            id_seccion__in=[d.id_seccion_id for d in Distribucion.objects.filter(id_distribucion__in=dist_ids)]
        ).distinct()
        
        secciones_con_materia = []
        for sec in secciones:
            dist = Distribucion.objects.filter(id_seccion=sec, id_profesor=id_profesor, estado=True).first()
            if dist:
                secciones_con_materia.append({
                    'seccion': sec,
                    'materia': dist.id_materia,
                    'id_distribucion': dist.id_distribucion
                })
    else:
        dists = Distribucion.objects.filter(estado=True).select_related('id_materia', 'id_seccion')
        secciones_con_materia = []
        for dist in dists:
            secciones_con_materia.append({
                'seccion': dist.id_seccion,
                'materia': dist.id_materia,
                'id_distribucion': dist.id_distribucion
            })
    
    return render(request, 'notas/menu.html', {
        'secciones_con_materia': secciones_con_materia,
        'rol_usuario': rol,
    })


def notas_por_seccion(request, id_distribucion):
    """Muestra la tabla de notas de una sección específica, organizada por tipo de evaluación."""
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor':
        dist_ids = _get_distribuciones_profesor(id_profesor)
        if id_distribucion not in dist_ids:
            messages.error(request, ' No tienes acceso a esta sección.')
            return redirect('notas:menu')
    
    distribucion = get_object_or_404(Distribucion, pk=id_distribucion, estado=True)
    seccion = distribucion.id_seccion
    materia = distribucion.id_materia
    

    estudiantes_data = []
    try:
        with connection.cursor() as cursor:
            seccion_id = seccion.id_seccion if hasattr(seccion, 'id_seccion') else seccion
            cursor.execute("""
                SELECT id_estudiante, cedula, nombre, apellido 
                FROM estudiantes 
                WHERE id_seccion = %s AND estado = 1
                ORDER BY apellido, nombre
            """, [seccion_id])
            
            for row in cursor.fetchall():
                estudiantes_data.append({
                    'id_estudiante': row[0],
                    'cedula': row[1],
                    'nombre': row[2],
                    'apellido': row[3]
                })
    except Exception as e:
        print(f"Error obteniendo estudiantes: {e}")
        messages.warning(request, 'No se pudieron cargar los estudiantes de esta sección.')
    
    tipos_evaluacion = ['Examen Parcial', 'Examen Final', 'Tarea', 'Proyecto', 'Laboratorio', 'Quizz', 'Participación']
    
    notas_data = []
    for est in estudiantes_data:
        estudiante_notas = {
            'id_estudiante': est['id_estudiante'],
            'nombre': f"{est['nombre']} {est['apellido']}",
            'cedula': est['cedula'],
            'periodos': {}
        }
        
        for tipo in tipos_evaluacion:
            periodos = {}

            for i, periodo in enumerate(['Periodo 1', 'Periodo 2', 'Periodo 3', 'Periodo 4'], 1):
                busqueda = f"{tipo} - {periodo}"
                nota = Nota.objects.filter(
                    id_distribucion=id_distribucion,
                    carnet_estudiante=est['cedula'],
                    tipo_evaluacion=busqueda,
                    estado=True
                ).first()
                
                if nota:
                    periodos[f'p{i}'] = nota.nota
                    periodos['id_nota'] = nota.id_nota
                else:
                    periodos[f'p{i}'] = None
            
            notas_validas = [v for k, v in periodos.items() if k.startswith('p') and v is not None]
            periodos['promedio'] = sum(notas_validas) / 4 if notas_validas else None
            
            estudiante_notas['periodos'][tipo] = periodos
        
        notas_data.append(estudiante_notas)
    
    return render(request, 'notas/detalle_seccion.html', {
        'distribucion': distribucion,
        'seccion': seccion,
        'materia': materia,
        'estudiantes': notas_data,
        'tipos_evaluacion': tipos_evaluacion,
        'rol_usuario': rol,
    })


def buscar_estudiante(request):
    """Busca estudiantes por NIE/nombre, filtrados por sección."""
    query = request.GET.get('q', '')
    seccion_id = request.GET.get('seccion_id', '')

    if seccion_id:
        try:
            seccion_id = parse_integer_at_least(
                seccion_id, 'La sección', minimum=1
            )
        except ValueError as error:
            return JsonResponse(
                {'estudiantes': [], 'error': str(error)},
                status=400,
            )

    if len(query) < 2:
        return JsonResponse({'estudiantes': []})
    
    try:
        with connection.cursor() as cursor:
            if seccion_id:
                cursor.execute("""
                    SELECT cedula, CONCAT(nombre, ' ', apellido) as nombre_completo
                    FROM estudiantes 
                    WHERE id_seccion = %s 
                      AND (cedula LIKE %s OR CONCAT(nombre, ' ', apellido) LIKE %s)
                      AND estado = 1
                    ORDER BY nombre
                    LIMIT 10
                """, [seccion_id, f'%{query}%', f'%{query}%'])
            else:
                cursor.execute("""
                    SELECT cedula, CONCAT(nombre, ' ', apellido) as nombre_completo
                    FROM estudiantes 
                    WHERE cedula LIKE %s OR CONCAT(nombre, ' ', apellido) LIKE %s
                      AND estado = 1
                    ORDER BY nombre
                    LIMIT 10
                """, [f'%{query}%', f'%{query}%'])
            
            resultados = [
                {'carnet': row[0], 'nombre': row[1]}
                for row in cursor.fetchall()
            ]
        return JsonResponse({'estudiantes': resultados})
    except Exception as e:
        print(f"ERROR buscar_estudiante: {e}")
        return JsonResponse({'estudiantes': [], 'error': str(e)})


def crear_nota(request, id_distribucion):
    """Crear nota para un estudiante específico en una distribución."""
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Profesor':
        dist_ids = _get_distribuciones_profesor(id_profesor)
        if id_distribucion not in dist_ids:
            messages.error(request, ' No tienes acceso a esta sección.')
            return redirect('notas:menu')
    
    distribucion = get_object_or_404(Distribucion, pk=id_distribucion, estado=True)
    
    if request.method == 'POST':
        carnet = request.POST.get('carnet_estudiante', '').strip()
        nombre_estudiante = request.POST.get('nombre_estudiante', '').strip()
        tipo_evaluacion = request.POST.get('tipo_evaluacion', '').strip()
        nota_raw = request.POST.get('nota', '').strip()
        if not nota_raw:
            messages.error(request, 'La calificación es obligatoria.')
            return redirect('notas:crear', id_distribucion=id_distribucion)
        try:
            nota_val = float(parse_decimal_at_least(
                nota_raw, 'La calificación', maximum=10
            ))
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('notas:crear', id_distribucion=id_distribucion)
        
        if carnet and nombre_estudiante and tipo_evaluacion:
            Nota.objects.create(
                id_distribucion=id_distribucion,
                carnet_estudiante=carnet,
                nombre_estudiante=nombre_estudiante,
                tipo_evaluacion=tipo_evaluacion,
                nota=nota_val,
                estado=True
            )
            messages.success(request, ' Nota registrada exitosamente')
            return redirect('notas:detalle_seccion', id_distribucion=id_distribucion)
        else:
            messages.error(request, ' Completa todos los campos obligatorios.')
    
    return render(request, 'notas/form.html', {
        'distribucion': distribucion,
        'rol_usuario': rol,
    })


def editar_nota(request, pk):
    """Editar una nota existente."""
    rol, user_id, id_profesor = _get_user_info(request)
    nota = get_object_or_404(Nota, pk=pk)
    
    if not rol:
        return redirect('/login/')
    
    if rol == 'Secretaria':
        messages.error(request, ' No tienes permisos para editar notas.')
        return redirect('notas:menu')
    
    if rol == 'Profesor':
        dist_ids = _get_distribuciones_profesor(id_profesor)
        if nota.id_distribucion not in dist_ids:
            messages.error(request, ' No puedes editar notas que no te corresponden.')
            return redirect('notas:menu')
    
    if request.method == 'POST':
        nota_raw = request.POST.get('nota', '').strip()
        if not nota_raw:
            messages.error(request, 'La calificación es obligatoria.')
            return redirect('notas:editar', pk=pk)
        try:
            nota.nota = float(parse_decimal_at_least(
                nota_raw, 'La calificación', maximum=10
            ))
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('notas:editar', pk=pk)
        nota.save()
        messages.success(request, ' Nota actualizada exitosamente')
        return redirect('notas:detalle_seccion', id_distribucion=nota.id_distribucion)
    
    return render(request, 'notas/form_editar.html', {
        'nota': nota,
        'rol_usuario': rol,
    })


def eliminar_nota(request, pk):
    """Eliminar (desactivar) una nota."""
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol:
        return redirect('/login/')
    
    if rol in ['Profesor', 'Secretaria']:
        messages.error(request, ' No tienes permisos para eliminar notas.')
        return redirect('notas:menu')
    
    nota = get_object_or_404(Nota, pk=pk)
    nota.estado = False
    nota.save()
    messages.success(request, ' Nota eliminada exitosamente')
    return redirect('notas:detalle_seccion', id_distribucion=nota.id_distribucion)


@csrf_exempt
@require_POST
def guardar_nota_ajax(request):
    """Guarda o actualiza una nota vía AJAX (edición inline)."""
    rol, user_id, id_profesor = _get_user_info(request)
    
    if not rol or rol == 'Secretaria':
        return JsonResponse({'success': False, 'error': 'No tienes permisos'})
    
    try:
        data = json.loads(request.body)
        id_distribucion = parse_integer_at_least(
            data.get('id_distribucion'), 'La distribución', minimum=1
        )
        carnet = str(data.get('carnet', '')).strip()
        tipo_evaluacion = str(data.get('tipo_evaluacion', '')).strip()
        nota_raw = data.get('nota')

        nota_vacia = nota_raw is None or str(nota_raw).strip() == ''
        if not nota_vacia:
            try:
                nota_valor = float(parse_decimal_at_least(
                    nota_raw, 'La calificación', maximum=10
                ))
            except ValueError as error:
                return JsonResponse({
                    'success': False, 
                    'error': str(error)
                })

        if not carnet or not tipo_evaluacion:
            return JsonResponse({'success': False, 'error': 'Faltan datos obligatorios (distribución, carnet o tipo)'})
        
        if rol == 'Profesor':
            dist_ids = _get_distribuciones_profesor(id_profesor)
            if id_distribucion not in dist_ids:
                return JsonResponse({'success': False, 'error': 'No tienes acceso a esta distribución'})
        

        nota_existente = Nota.objects.filter(
            id_distribucion=id_distribucion,
            carnet_estudiante=carnet,
            tipo_evaluacion=tipo_evaluacion,
            estado=True
        ).first()
        
        if nota_existente:
            if nota_vacia:
                nota_existente.estado = False
                nota_existente.save()
                return JsonResponse({
                    'success': True,
                    'mensaje': 'Nota eliminada',
                    'nota': None,
                    'carnet': carnet,
                    'tipo': tipo_evaluacion
                })
            nota_existente.nota = nota_valor
            nota_existente.save()
            mensaje = 'Nota actualizada'
        else:
            if nota_vacia:
                return JsonResponse({
                    'success': True,
                    'mensaje': 'No hay nota para eliminar',
                    'nota': None,
                    'carnet': carnet,
                    'tipo': tipo_evaluacion
                })

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT CONCAT(nombre, ' ', apellido) FROM estudiantes WHERE cedula = %s", 
                    [carnet]
                )
                row = cursor.fetchone()
                nombre_estudiante = row[0] if row else 'Estudiante Desconocido'
            
            Nota.objects.create(
                id_distribucion=id_distribucion,
                carnet_estudiante=carnet,
                nombre_estudiante=nombre_estudiante,
                tipo_evaluacion=tipo_evaluacion,
                nota=nota_valor,
                estado=True
            )
            mensaje = 'Nota creada'
        
        return JsonResponse({
            'success': True, 
            'mensaje': mensaje, 
            'nota': nota_valor,
            'carnet': carnet,
            'tipo': tipo_evaluacion
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos JSON inválidos'})
    except ValueError as error:
        return JsonResponse({'success': False, 'error': str(error)}, status=400)
    except Exception as e:

        print(f" ERROR CRÍTICO en guardar_nota_ajax: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': f'Error interno: {str(e)}'})