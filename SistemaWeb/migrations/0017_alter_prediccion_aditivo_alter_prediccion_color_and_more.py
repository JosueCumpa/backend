# Generated by Django 4.2.7 on 2024-08-20 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SistemaWeb', '0016_prediccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediccion',
            name='aditivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aditivo', to='SistemaWeb.materiaprima'),
        ),
        migrations.AlterField(
            model_name='prediccion',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='SistemaWeb.materiaprima'),
        ),
        migrations.AlterField(
            model_name='prediccion',
            name='operario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operario_prediccion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prediccion',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable_prediccion', to=settings.AUTH_USER_MODEL),
        ),
    ]
