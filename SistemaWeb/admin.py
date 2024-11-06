from django.contrib import admin
from .models import TipoProducto, MaquinaInyeccion, Producto, Categoria, MateriaPrima, Turno, LabelEncoderTable

admin.site.register(TipoProducto)
admin.site.register(MaquinaInyeccion)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(MateriaPrima)
admin.site.register(Turno)
admin.site.register(LabelEncoderTable)