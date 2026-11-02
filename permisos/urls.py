from django.urls import path
from . import views

app_name = 'permisos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:id_permiso>/', views.editar, name='editar'),
    path('eliminar/<int:id_permiso>/', views.eliminar, name='eliminar'),
]