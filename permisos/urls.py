from django.urls import path
from . import views

app_name = 'permisos' 

urlpatterns = [
    path('', views.lista_permisos, name='lista'),
    path('crear/', views.crear_permiso, name='crear'),
]