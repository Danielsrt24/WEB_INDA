

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id_seccion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('nivel', models.CharField(max_length=20)),
                ('letra', models.CharField(max_length=5)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'secciones',
                'ordering': ['nivel', 'letra'],
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id_estudiante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1)),
                ('estado', models.BooleanField(default=True)),
                ('id_seccion', models.ForeignKey(db_column='id_seccion', on_delete=django.db.models.deletion.CASCADE, related_name='estudiantes', to='secciones.seccion')),
            ],
            options={
                'db_table': 'estudiantes',
                'ordering': ['apellido', 'nombre'],
            },
        ),
    ]
