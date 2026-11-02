from django.db import models

class Distribucion(models.Model):
    id_distribucion = models.AutoField(primary_key=True)
    

    id_profesor = models.ForeignKey(
        'core.Profesor', 
        on_delete=models.CASCADE, 
        db_column='id_profesor',
        related_name='distribuciones'
    )
    id_materia = models.ForeignKey(
        'materias.Materia', 
        on_delete=models.CASCADE, 
        db_column='id_materia',
        related_name='distribuciones'
    )
    id_seccion = models.ForeignKey(
        'secciones.Seccion', 
        on_delete=models.CASCADE, 
        db_column='id_seccion',
        related_name='distribuciones'
    )
    
    horas_semanales = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'distribucion'

