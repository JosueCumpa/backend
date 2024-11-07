
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

#Tabla oculta .. solo base de datos para almacenar el valor del label enconder de la IA ejemplo: Sergio : 0
class LabelEncoderTable(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    categoria= models.CharField(max_length=150, null=False, blank=False)
    valor= models.IntegerField()
    def __str__(self):
        return self.valor

class Produccion(models.Model):
    cantidad_fabricada = models.IntegerField()
    rechazadas = models.IntegerField()
    operario = models.CharField(max_length=100)
    responsable_calidad = models.CharField(max_length=100)
    producto = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100)
    maquina = models.CharField(max_length=50)
    molde_macho = models.IntegerField()
    molde_hembra = models.IntegerField()
    c_producto = models.IntegerField()
    peso = models.FloatField()
    zona_1 = models.IntegerField()
    zona_2 = models.IntegerField()
    zona_3 = models.IntegerField()
    zona_4 = models.IntegerField()
    zona_5 = models.IntegerField()

    def __str__(self):
        return f'{self.producto} - {self.operario}'

class PrediccionV2(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    cantidad = models.IntegerField()
    operario = models.ForeignKey(User, related_name='operario_prediccion_v2', on_delete=models.CASCADE)
    res_calidad = models.ForeignKey(User, related_name='responsable_prediccion_v2', on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    maquina = models.ForeignKey(MaquinaInyeccion, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    producto =  models.ForeignKey(Producto, on_delete=models.CASCADE)
    aditivo = models.ForeignKey(MateriaPrima, related_name='aditivo', on_delete=models.CASCADE)
    cantidad_mp = models.DecimalField(max_digits=5, decimal_places=2)  # Campo para "Cantidad MP(KG)"
    cantidad_aditivo = models.DecimalField(max_digits=4, decimal_places=2)  # Campo para "Cantidad Aditivo(KG)"
    cantidad_merma = models.IntegerField()  # Campo para "Cantidad Merma(gr)"
    largo = models.DecimalField(max_digits=4, decimal_places=2)    # Campo para "Ingrese L(cm)"
    ancho = models.DecimalField(max_digits=3, decimal_places=2)  # Campo para "Ingrese A(cm)"
    ciclos = models.IntegerField()  # Campo para "Ciclos (seg)"
    peso_prensada = models.DecimalField(max_digits=5, decimal_places=2, default=120)  # Campo para "Peso (gr) Prensada"
    color = models.ForeignKey(MateriaPrima, related_name='color', on_delete=models.CASCADE)  # Campo para seleccionar colores
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)  # Campo para seleccionar materia prima
    prediccion_promedio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Predicción del {self.fecha} - Producto: {self.producto}"

class DetallePrediccion(models.Model):
    prediccion = models.ForeignKey(PrediccionV2, related_name='detalles', on_delete=models.CASCADE)
    rechazos = models.IntegerField()  # Cantidad de piezas rechazadas
    molde_macho = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura del molde macho (°C)
    molde_hembra = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura del molde hembra (°C)
    temp_producto = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura del producto (°C)
    zona_1 = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura zona 1 (°C)
    zona_2 = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura zona 2 (°C)
    zona_3 = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura zona 3 (°C)
    zona_4 = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura zona 4 (°C)
    zona_5 = models.DecimalField(max_digits=5, decimal_places=2)  # Temperatura zona 5 (°C)
    calidad = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de calidad (%)

    def __str__(self):
        return f"Detalle de Predicción {self.prediccion} - Calidad: {self.calidad}%"

class Recomendacion(models.Model):
    prediccion = models.ForeignKey(PrediccionV2, on_delete=models.CASCADE)
    operario = models.CharField(max_length=255)
    responsable = models.CharField(max_length=255)
    maquina = models.CharField(max_length=255)
    temp_molde_macho = models.FloatField()
    temp_molde_hembra = models.FloatField()
    temp_c_producto = models.FloatField(default=0.0)
    zona_1 = models.FloatField()
    zona_2 = models.FloatField()
    zona_3 = models.FloatField()
    zona_4 = models.FloatField()
    zona_5 = models.FloatField()
    valorPrediction= models.FloatField( default=0.0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Recomendación {self.id} - {self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")}'
