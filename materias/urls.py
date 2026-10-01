from django.urls import path
from . import views

app_name = 'materias'

urlpatterns = [
    path('', views.lista_materias, name='lista'),
    path('crear/', views.crear_materia, name='crear'),
    path('<int:pk>/editar/', views.editar_materia, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_materia, name='eliminar'),
]