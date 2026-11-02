from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('', include('core.urls')),
    

    path('materias/', include('materias.urls')),
    path('permisos/', include('permisos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('distribucion/', include('distribucion.urls')),
    path('horario/', include('horario.urls')),
    path('secciones/', include('secciones.urls')),
    path('notas/', include('notas.urls')),
    path('reportes/', include('reportes.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)