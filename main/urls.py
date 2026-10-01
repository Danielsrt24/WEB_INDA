# web/main/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
        path('', include('core.urls')),
    
    path('materias/', include('materias.urls')),
    
    # Los demás módulos los dejamos comentados hasta que los programemos
    path('permisos/', include('permisos.urls')),
    path('usuarios/', include('usuarios.urls')),
    # path('distribucion/', include('distribucion.urls')),
    # path('horario/', include('horario.urls')),
    # path('secciones/', include('secciones.urls')),
    # path('notas/', include('notas.urls')),
]