
from django.db import models

class MaquinaInyeccion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    estado = models.CharField(max_length=1)

    def __str__(self):
        return self.nombre