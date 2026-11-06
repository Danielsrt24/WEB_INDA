import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_time
from core.validation import parse_integer_at_least

API_URL = "http://127.0.0.1:8000/api"


def _es_profesor(request):
    """Verifica si el usuario actual es Profesor."""
    return request.session.get('rol') == 'Profesor'






def lista_horarios(request):
    """Muestra la lista de todos los horarios."""
    try:
        response = requests.get(f"{API_URL}/horario/")
        response.raise_for_status()
        horarios = response.json()
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')
        horarios = []
    
    return render(request, 'horario/lista.html', {
        'horarios': horarios,
        'es_profesor': _es_profesor(request),
    })


def crear(request):
    """Crea un nuevo horario."""
    rol = request.session.get('rol')
    
    if not rol:
        return redirect('/login/')
    
    if request.method == 'POST':
        id_distribucion = request.POST.get('id_distribucion')
        dia = request.POST.get('dia')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        aula = request.POST.get('aula', '').strip()
        
        try:
            id_distribucion = parse_integer_at_least(
                id_distribucion, 'La distribución', minimum=1
            )
        except ValueError as error:
            messages.error(request, str(error))
            return redirect('horario:crear')

        hora_inicio = parse_time(hora_inicio) if hora_inicio else None
        hora_fin = parse_time(hora_fin) if hora_fin else None
        if hora_inicio is None or hora_fin is None or hora_inicio >= hora_fin:
            messages.error(
                request,
                'Las horas deben ser válidas y la hora de inicio debe ser anterior a la hora de fin.',
            )
            return redirect('horario:crear')

        if dia and hora_inicio and hora_fin:
            from .models import Horario
            Horario.objects.create(
                id_distribucion_id=int(id_distribucion),
                dia=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                aula=aula
            )
            messages.success(request, ' Horario creado exitosamente')
            return redirect('/horario/')
        else:
            messages.error(request, ' Completa todos los campos obligatorios')
    

    from distribucion.models import Distribucion
    

    distribuciones = Distribucion.objects.select_related('id_profesor', 'id_materia', 'id_seccion').all()
    
    return render(request, 'horario/crear.html', {
        'distribuciones': distribuciones,
        'rol_usuario': rol,
    })


def tabla_horario(request):
    """Muestra el horario en formato de tabla visual."""
    try:
        response = requests.get(f"{API_URL}/horario/")
        response.raise_for_status()
        horarios = response.json()
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')
        horarios = []
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = {}
    
    for h in horarios:
        dia = h.get('dia')
        if dia not in horas:
            horas[dia] = []
        horas[dia].append(h)

    filas_horario = [
        {'dia': dia, 'horarios': horas.get(dia, [])}
        for dia in dias
    ]
    
    return render(request, 'horario/tabla.html', {
        'filas_horario': filas_horario,
        'es_profesor': _es_profesor(request),
    })






def menu_horarios(request):
    """Muestra el menú principal de horarios con las dos opciones."""
    return render(request, 'horario/menu.html', {
        'es_profesor': _es_profesor(request),
    })






def lista_secciones_horario(request):
    """Muestra la lista de todas las secciones para elegir una."""
    try:
        response = requests.get(f"{API_URL}/secciones/")
        response.raise_for_status()
        secciones = response.json()
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')
        secciones = []
    return render(request, 'horario/lista_secciones.html', {'secciones': secciones})


def lista_profesores_horario(request):
    """Muestra la lista de todos los profesores para elegir uno."""
    try:
        response = requests.get(f"{API_URL}/profesores/")
        response.raise_for_status()
        profesores = response.json()
    except Exception as e:
        messages.error(request, f'Error al conectar con la API: {str(e)}')
        profesores = []
    return render(request, 'horario/lista_profesores.html', {'profesores': profesores})






def horario_por_seccion(request, seccion_id):
    """Muestra el horario específico de una sección."""
    try:
        response_hor = requests.get(f"{API_URL}/horario/seccion/{seccion_id}")
        response_hor.raise_for_status()
        horarios = response_hor.json()
        
        response_sec = requests.get(f"{API_URL}/secciones/{seccion_id}")
        nombre_entidad = response_sec.json().get('nombre', f'Sección #{seccion_id}') if response_sec.status_code == 200 else f'Sección #{seccion_id}'
        
        response_dist = requests.get(f"{API_URL}/distribucion/")
        distribuciones = response_dist.json() if response_dist.status_code == 200 else []
        
        response_prof = requests.get(f"{API_URL}/profesores/")
        profesores = response_prof.json() if response_prof.status_code == 200 else []
        
        response_mat = requests.get(f"{API_URL}/materias/")
        materias = response_mat.json() if response_mat.status_code == 200 else []
        
        prof_map = {p['id_profesor']: p['nombre'] for p in profesores}
        
        mat_map = {}
        for m in materias:
            mat_id = m.get('id_materia')
            nombre_mat = m.get('nombre') or m.get('codigo') or f'Materia #{mat_id}'
            mat_map[mat_id] = nombre_mat
        
        dist_map = {}
        for dist in distribuciones:
            id_prof = dist.get('id_profesor')
            id_mat = dist.get('id_materia')
            dist_map[dist['id_distribucion']] = {
                'profesor': prof_map.get(id_prof, 'Sin asignar'),
                'materia': mat_map.get(id_mat, 'Sin asignar')
            }
        
        horarios_enriquecidos = []
        for h in horarios:
            horario_con_info = h.copy()
            dist_info = dist_map.get(h.get('id_distribucion'), {})
            horario_con_info['nombre_profesor'] = dist_info.get('profesor', 'Sin asignar')
            horario_con_info['nombre_materia'] = dist_info.get('materia', 'Sin asignar')
            horarios_enriquecidos.append(horario_con_info)
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        horarios_enriquecidos = []
        nombre_entidad = f'Sección #{seccion_id}'

    return render(request, 'horario/detalle.html', {
        'horarios': horarios_enriquecidos,
        'tipo': 'Sección',
        'entidad_nombre': nombre_entidad,
        'entidad_id': seccion_id
    })


def horario_por_profesor(request, profesor_id):
    """Muestra el horario específico de un profesor."""
    try:
        response_hor = requests.get(f"{API_URL}/horario/profesor/{profesor_id}")
        response_hor.raise_for_status()
        horarios = response_hor.json()
        
        response_prof = requests.get(f"{API_URL}/profesores/{profesor_id}")
        nombre_entidad = response_prof.json().get('nombre', f'Profesor #{profesor_id}') if response_prof.status_code == 200 else f'Profesor #{profesor_id}'
        
        response_dist = requests.get(f"{API_URL}/distribucion/")
        distribuciones = response_dist.json() if response_dist.status_code == 200 else []
        
        response_mat = requests.get(f"{API_URL}/materias/")
        materias = response_mat.json() if response_mat.status_code == 200 else []
        
        response_sec = requests.get(f"{API_URL}/secciones/")
        secciones = response_sec.json() if response_sec.status_code == 200 else []
        
        mat_map = {}
        for m in materias:
            mat_id = m.get('id_materia')
            nombre_mat = m.get('nombre') or m.get('codigo') or f'Materia #{mat_id}'
            mat_map[mat_id] = nombre_mat
        
        sec_map = {}
        for s in secciones:
            sec_id = s.get('id_seccion')
            nombre_sec = s.get('nombre') or s.get('codigo') or f'Sección #{sec_id}'
            sec_map[sec_id] = nombre_sec
        
        dist_map = {}
        for dist in distribuciones:
            id_mat = dist.get('id_materia')
            id_sec = dist.get('id_seccion')
            dist_map[dist['id_distribucion']] = {
                'materia': mat_map.get(id_mat, 'Sin asignar'),
                'seccion': sec_map.get(id_sec, 'N/A')
            }
        
        horarios_enriquecidos = []
        for h in horarios:
            horario_con_info = h.copy()
            dist_info = dist_map.get(h.get('id_distribucion'), {})
            horario_con_info['nombre_materia'] = dist_info.get('materia', 'Sin asignar')
            horario_con_info['nombre_seccion'] = dist_info.get('seccion', 'N/A')
            horarios_enriquecidos.append(horario_con_info)
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        horarios_enriquecidos = []
        nombre_entidad = f'Profesor #{profesor_id}'

    return render(request, 'horario/detalle.html', {
        'horarios': horarios_enriquecidos,
        'tipo': 'Profesor',
        'entidad_nombre': nombre_entidad,
        'entidad_id': profesor_id
    })