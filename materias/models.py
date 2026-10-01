from django.db import models

class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'materias'
        managed = False

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"