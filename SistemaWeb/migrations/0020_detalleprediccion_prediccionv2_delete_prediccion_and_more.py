# Generated by Django 4.2.7 on 2024-10-08 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SistemaWeb', '0019_produccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePrediccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rechazos', models.IntegerField()),
                ('molde_macho', models.DecimalField(decimal_places=2, max_digits=5)),
                ('molde_hembra', models.DecimalField(decimal_places=2, max_digits=5)),
                ('temp_producto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('zona_1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('zona_2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('zona_3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('zona_4', models.DecimalField(decimal_places=2, max_digits=5)),
                ('zona_5', models.DecimalField(decimal_places=2, max_digits=5)),
                ('calidad', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='PrediccionV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('cantidad', models.IntegerField()),
                ('cantidad_mp', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cantidad_aditivo', models.DecimalField(decimal_places=2, max_digits=4)),
                ('cantidad_merma', models.IntegerField()),
                ('largo', models.DecimalField(decimal_places=2, max_digits=4)),
                ('ancho', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ciclos', models.IntegerField()),
                ('peso_prensada', models.DecimalField(decimal_places=2, max_digits=5)),
                ('aditivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aditivo', to='SistemaWeb.materiaprima')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='SistemaWeb.materiaprima')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.maquinainyeccion')),
                ('materia_prima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.materiaprima')),
                ('operario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operario_prediccion_v2', to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.producto')),
                ('res_calidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_prediccion_v2', to=settings.AUTH_USER_MODEL)),
                ('tipo_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.tipoproducto')),
                ('turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.turno')),
            ],
        ),
        migrations.DeleteModel(
            name='Prediccion',
        ),
        migrations.AddField(
            model_name='detalleprediccion',
            name='prediccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='SistemaWeb.prediccionv2'),
        ),
    ]