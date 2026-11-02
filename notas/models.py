from django.db import models

class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    id_distribucion = models.IntegerField(help_text="ID de la distribución (profesor-materia-sección)")
    carnet_estudiante = models.CharField(max_length=20, help_text="Carnet del estudiante")
    nombre_estudiante = models.CharField(max_length=150, help_text="Nombre completo del estudiante")
    tipo_evaluacion = models.CharField(max_length=50, help_text="Ej: Examen Parcial, Tarea, Proyecto")
    nota = models.FloatField(help_text="Calificación (0-100)")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True, help_text="1=Activo, 0=Inactivo")

    class Meta:
        db_table = 'notas'
        managed = False

    def __str__(self):
        return f"Nota {self.nota} - {self.nombre_estudiante}"