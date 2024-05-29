
from django.db import models

class MaquinaInyeccion(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('M', 'Mantenimiento'),
    ] 
    nombre = models.CharField(max_length=150, unique=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.nombre

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=150,blank=True)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=150,blank=True)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre= models.CharField(max_length=150)
    descripcion= models.CharField(max_length=150, blank=True)
    estado= models.BooleanField()
    tipoPro= models.ForeignKey(TipoProducto, null=True, blank=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.nombre

class MateriaPrima(models.Model):
    nombre= models.CharField(max_length=150)
    descripcion= models.CharField(max_length=150, blank=True)
    estado= models.BooleanField()
    categoria= models.ForeignKey(Categoria, null=True, blank=True, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Turno(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre