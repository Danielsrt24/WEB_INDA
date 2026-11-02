from django.db import models

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    id_profesor = models.IntegerField()
    tipo_permiso = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(blank=True, null=True)
    horas_afectadas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, default='pendiente')
    id_usuario_registro = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    comprobante = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'permisos'
        managed = False

    def __str__(self):
        return f"Permiso #{self.id_permiso} - {self.tipo_permiso}"