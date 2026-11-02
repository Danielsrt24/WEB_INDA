

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id_permiso', models.AutoField(primary_key=True, serialize=False)),
                ('id_profesor', models.IntegerField()),
                ('tipo_permiso', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('motivo', models.TextField(blank=True, null=True)),
                ('horas_afectadas', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('estado', models.CharField(default='pendiente', max_length=20)),
                ('id_usuario_registro', models.IntegerField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'permisos',
                'managed': False,
            },
        ),
    ]
