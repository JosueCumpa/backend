# Generated by Django 4.2.7 on 2024-10-18 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaWeb', '0024_recomendacion_valorprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='recomendacion',
            name='temp_c_producto',
            field=models.FloatField(default=0.0),
        ),
    ]
