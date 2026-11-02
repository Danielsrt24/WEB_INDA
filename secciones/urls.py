from django.urls import path
from . import views

app_name = 'secciones'

urlpatterns = [
    path('', views.lista_secciones, name='lista'),
    path('crear/', views.crear_seccion, name='crear'),
    path('<int:pk>/editar/', views.editar_seccion, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_seccion, name='eliminar'),
    path('<int:seccion_id>/estudiantes/', views.lista_estudiantes, name='estudiantes'),
    path('<int:seccion_id>/estudiantes/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiante/<int:pk>/editar/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiante/<int:pk>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
]