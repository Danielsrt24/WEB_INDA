from django.urls import path
from . import views

app_name = 'distribucion'

urlpatterns = [
    path('', views.lista_distribucion, name='lista'),
    path('crear/', views.crear_distribucion, name='crear'),
    path('<int:pk>/editar/', views.editar_distribucion, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_distribucion, name='eliminar'),
]