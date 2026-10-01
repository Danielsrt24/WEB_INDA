from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('Director', 'Director'),
        ('Subdirector', 'Subdirector'),
        ('Secretaria', 'Secretaria'),
        ('Profesor', 'Profesor'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    nombre = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=ROLES)
    email = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        managed = False  

    def __str__(self):
        return f"{self.username} ({self.rol})"