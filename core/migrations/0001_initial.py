

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=150)),
                ('rol', models.CharField(choices=[('Director', 'Director'), ('Subdirector', 'Subdirector'), ('Secretaria', 'Secretaria'), ('Profesor', 'Profesor')], max_length=20)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'usuarios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id_profesor', models.AutoField(primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'profesores',
            },
        ),
    ]
