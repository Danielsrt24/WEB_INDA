from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.menu_reportes, name='menu'),
    path('notas/', views.reporte_notas, name='notas'),
    path('permisos/', views.reporte_permisos, name='permisos'),
    path('estudiantes/', views.reporte_estudiantes, name='estudiantes'),
]