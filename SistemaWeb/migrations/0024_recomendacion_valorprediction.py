# Generated by Django 4.2.7 on 2024-10-18 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaWeb', '0023_recomendacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='recomendacion',
            name='valorPrediction',
            field=models.FloatField(default=0.0),
        ),
    ]