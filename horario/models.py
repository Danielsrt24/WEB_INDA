from django.db import models
from distribucion.models import Distribucion

class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    id_distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE, db_column='id_distribucion')
    dia = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'horario'
        managed = False

    def __str__(self):
        return f"{self.dia} {self.hora_inicio} - {self.hora_fin}"