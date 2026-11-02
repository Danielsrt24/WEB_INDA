

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('secciones', '0001_initial'),
        ('materias', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribucion',
            fields=[
                ('id_distribucion', models.AutoField(primary_key=True, serialize=False)),
                ('horas_semanales', models.IntegerField(default=0)),
                ('estado', models.BooleanField(default=True)),
                ('id_materia', models.ForeignKey(db_column='id_materia', on_delete=django.db.models.deletion.CASCADE, related_name='distribuciones', to='materias.materia')),
                ('id_profesor', models.ForeignKey(db_column='id_profesor', on_delete=django.db.models.deletion.CASCADE, related_name='distribuciones', to='core.profesor')),
                ('id_seccion', models.ForeignKey(db_column='id_seccion', on_delete=django.db.models.deletion.CASCADE, related_name='distribuciones', to='secciones.seccion')),
            ],
            options={
                'db_table': 'distribucion',
            },
        ),
    ]
