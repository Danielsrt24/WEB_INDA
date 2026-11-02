from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.menu_notas, name='menu'),
    path('seccion/<int:id_distribucion>/', views.notas_por_seccion, name='detalle_seccion'),
    path('seccion/<int:id_distribucion>/crear/', views.crear_nota, name='crear'),
    path('guardar-nota-ajax/', views.guardar_nota_ajax, name='guardar_nota_ajax'),
    path('<int:pk>/editar/', views.editar_nota, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_nota, name='eliminar'),
    path('buscar-estudiante/', views.buscar_estudiante, name='buscar_estudiante'),
]