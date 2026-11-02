from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    username = models.CharField(max_length=100, db_column='username')
    password_hash = models.CharField(max_length=255, db_column='password_hash')
    nombre = models.CharField(max_length=150, db_column='nombre')
    rol = models.CharField(max_length=50, db_column='rol')
    email = models.CharField(max_length=150, blank=True, null=True, db_column='email')
    estado = models.IntegerField(default=1, db_column='estado')
    fecha_registro = models.DateTimeField(auto_now_add=True, db_column='fecha_registro')
    id_profesor = models.IntegerField(blank=True, null=True, db_column='id_profesor')

    class Meta:
        db_table = 'usuarios'
        managed = False

    def __str__(self):
        return f"{self.username} ({self.rol})"