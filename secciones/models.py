from django.db import models

class Seccion(models.Model):
    id_seccion = models.AutoField(primary_key=True, db_column='id_seccion')
    nombre = models.CharField(max_length=100, db_column='nombre')
    nivel = models.CharField(max_length=50, blank=True, null=True, db_column='nivel')
    letra = models.CharField(max_length=10, blank=True, null=True, db_column='letra')
    estado = models.BooleanField(default=True, db_column='estado')
    
    class Meta:
        db_table = 'secciones'
        managed = False
    
    def __str__(self):
        return f"{self.nombre} - {self.nivel} {self.letra or ''}"


class Estudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    id_seccion = models.ForeignKey(
        Seccion, 
        on_delete=models.CASCADE, 
        related_name='estudiantes',
        db_column='id_seccion'
    )
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'estudiantes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.id_seccion.nombre})"