from django.urls import path
from . import views

app_name = 'horario'

urlpatterns = [

    path('', views.lista_horarios, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('tabla/', views.tabla_horario, name='tabla'),
    

    path('menu/', views.menu_horarios, name='menu'),
    

    path('secciones/', views.lista_secciones_horario, name='lista_secciones'),
    path('profesores/', views.lista_profesores_horario, name='lista_profesores'),
    

    path('seccion/<int:seccion_id>/', views.horario_por_seccion, name='por_seccion'),
    path('profesor/<int:profesor_id>/', views.horario_por_profesor, name='por_profesor'),
]