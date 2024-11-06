from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from . serializers import UserSerializer, MaquinaSerializer,TipoProductoSerializer, ProductoSerializer, CategoriaSerializer,TurnoSerializer, RecomendacionSerializer,MateriaPrimaSerializer,PrediccionV2Serializer,DetallePrediccionSerializer
from .models import MaquinaInyeccion,TipoProducto, Producto, Categoria, MateriaPrima, Turno, LabelEncoderTable,PrediccionV2,DetallePrediccion, Recomendacion
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from collections import defaultdict
from .model_loader import modelo
from datetime import datetime, timedelta
import numpy as np
from django.db.models import Sum, Count
from django.utils import timezone
from django.db import connection
import random

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data.get('username'))

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {
                "user_data": {
                    "name": user.first_name + " " + user.last_name,
                    "group": "true" if user.is_superuser else "false",
                    "op": "true" if user.is_staff else "false",
                },
                "tokens": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )

#MAQUINA----------------------------------------------
class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = MaquinaInyeccion.objects.all()
    serializer_class = MaquinaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

#TIPO DE PRODUCTO ----------------------------------------------
class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]     

class ListaTproductoActivoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        tipos_productos = TipoProducto.objects.filter(estado=True)
        serializer = TipoProductoSerializer(tipos_productos, many=True)
        return Response(serializer.data)

#TURNO ----------------------------------------------
class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class= TurnoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

#CATEGORIA ----------------------------------------------------
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset= Categoria.objects.all()
    serializer_class = CategoriaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ListaCategoriaActivoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        categorias= Categoria.objects.filter(estado= True)
        serializer = CategoriaSerializer(categorias, many= True)
        return Response(serializer.data)

#Producto----------------------------------------------
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto registrado correctamente'}, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

#MateriaPrima----------------------------------------------
class MateriaPrimaViewSet(viewsets.ModelViewSet):
    queryset= MateriaPrima.objects.all()
    serializer_class= MateriaPrimaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Materia Prima registrada correctamente'}, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# #Predicciones---------------------------------------------

class PrediccionV2ViewSet(viewsets.ModelViewSet):
    queryset = PrediccionV2.objects.all()
    serializer_class = PrediccionV2Serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class DetallePrediccionViewSet(viewsets.ModelViewSet):
    queryset = DetallePrediccion.objects.all()
    serializer_class = DetallePrediccionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class RecomendacionIDAPIView(APIView):
    def get(self, request, prediccion_id):
        # Filtrar las recomendaciones según el ID de la predicción
        detalles = Recomendacion.objects.filter(prediccion_id=prediccion_id)
        if detalles.exists():
            serializer = RecomendacionSerializer(detalles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Recomendación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class DetallePrediccionPorIDAPIView(APIView):
    def get(self, request, prediccion_id):
        # Filtrar los detalles según el ID de la predicción
        detalles = DetallePrediccion.objects.filter(prediccion_id=prediccion_id)
        
        if detalles.exists():
            serializer = DetallePrediccionSerializer(detalles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontraron detalles para la predicción proporcionada.'}, status=status.HTTP_404_NOT_FOUND)


# class PrediccionViewSet(viewsets.ModelViewSet):
#     queryset= Prediccion.objects.all().order_by('-fecha_produccion')
#     serializer_class= PrediccionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

# class PrediccionChartDataView(APIView):
#     def get(self, request, *args, **kwargs):
#         current_year = datetime.now().year
#         tipo_producto = request.query_params.get('tipo_producto')
#         producto = request.query_params.get('producto')

#         # Filtrar por año actual y aplicar filtros si los parámetros existen
#         predicciones = Prediccion.objects.filter(
#             fecha_produccion__year=current_year
#         )

#         if tipo_producto:
#             predicciones = predicciones.filter(tipo_id=tipo_producto)
#         if producto:
#             predicciones = predicciones.filter(producto_id=producto)

#         serializer = PrediccionDataLineSerializer(predicciones, many=True)
#         data = serializer.data

#         # Agrupar datos por mes
#         grouped_data = defaultdict(lambda: {
#             'prediccion': 0, 
#             'v_real': 0, 
#             'cantidad_fabric': 0, 
#             'ciclo_seg': 0, 
#             'c_molde_macho': 0,
#             'c_molde_hembra': 0,
#             'zona_1': 0,
#             'zona_2': 0,
#             'zona_3': 0,
#             'zona_4': 0,
#             'zona_5': 0,
#             'c_product': 0,  # Nuevo campo agregado
#             'count': 0
#         })

#         for item in data:
#             fecha = item['fecha_produccion']
#             if fecha:
#                 month_year = datetime.strptime(fecha, '%Y-%m-%d').strftime('%b %y')
#                 grouped_data[month_year]['prediccion'] += item['prediccion']
#                 grouped_data[month_year]['v_real'] += item['v_real'] or 0
#                 grouped_data[month_year]['cantidad_fabric'] += item.get('cantidad_fabric', 0) or 0
#                 grouped_data[month_year]['ciclo_seg'] += item.get('ciclo_seg', 0) or 0
#                 grouped_data[month_year]['c_molde_macho'] += item.get('c_molde_macho', 0) or 0
#                 grouped_data[month_year]['c_molde_hembra'] += item.get('c_molde_hembra', 0) or 0
#                 grouped_data[month_year]['zona_1'] += item.get('zona_1', 0) or 0
#                 grouped_data[month_year]['zona_2'] += item.get('zona_2', 0) or 0
#                 grouped_data[month_year]['zona_3'] += item.get('zona_3', 0) or 0
#                 grouped_data[month_year]['zona_4'] += item.get('zona_4', 0) or 0
#                 grouped_data[month_year]['zona_5'] += item.get('zona_5', 0) or 0
#                 grouped_data[month_year]['c_product'] += item.get('c_product', 0) or 0  # Agregado el campo c_product
#                 grouped_data[month_year]['count'] += 1

#         # Preparar datos para todos los meses del año
#         all_months = [datetime(current_year, month, 1).strftime('%b %y') for month in range(1, 13)]
#         formatted_data = [
#             {
#                 'date': month,
#                 'prediccion': round(grouped_data.get(month, {'prediccion': 0, 'count': 1})['prediccion'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'v_real': round(grouped_data.get(month, {'v_real': 0, 'count': 1})['v_real'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'cantidad_fabricada': grouped_data.get(month, {'cantidad_fabric': 0})['cantidad_fabric'],
#                 'ciclo_seg': round(grouped_data.get(month, {'ciclo_seg': 0, 'count': 1})['ciclo_seg'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'T Molde Macho': round(grouped_data.get(month, {'c_molde_macho': 0, 'count': 1})['c_molde_macho'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'T Molde Hembra': round(grouped_data.get(month, {'c_molde_hembra': 0, 'count': 1})['c_molde_hembra'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'Zona 1': round(grouped_data.get(month, {'zona_1': 0, 'count': 1})['zona_1'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'Zona 2': round(grouped_data.get(month, {'zona_2': 0, 'count': 1})['zona_2'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'Zona 3': round(grouped_data.get(month, {'zona_3': 0, 'count': 1})['zona_3'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'Zona 4': round(grouped_data.get(month, {'zona_4': 0, 'count': 1})['zona_4'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'Zona 5': round(grouped_data.get(month, {'zona_5': 0, 'count': 1})['zona_5'] / grouped_data.get(month, {'count': 1})['count'], 1),
#                 'T Producto': round(grouped_data.get(month, {'c_product': 0, 'count': 1})['c_product'] / grouped_data.get(month, {'count': 1})['count'], 1)  # Agregado el campo c_product
#             }
#             for month in all_months
#         ]

#         return Response(formatted_data)
    
# class ProductFabricationCountView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Obtener el año actual
#         current_year = timezone.now().year
        
#         # Filtrar por el año actual y agrupar por nombre del producto
#         data = (
#             Prediccion.objects
#             .filter(fecha_produccion__year=current_year)
#             .values('producto__nombre')
#             .annotate(cantidad_fabric=Sum('cantidad_fabric'))
#             .order_by('-cantidad_fabric')  # Ordenar de mayor a menor
#         )
        
#         # Transformar el queryset en una lista de diccionarios
#         formatted_data = [{'producto': item['producto__nombre'], 'cantidad_fabric': item['cantidad_fabric']} for item in data]
        
#         return Response(formatted_data, status=status.HTTP_200_OK)

# class Top5MaterialsView(APIView):
   

def obtener_valores_min_max(cantidad_fabricada, operario, producto ):
    with connection.cursor() as cursor:
        # Ejecutar la consulta SQL con los valores pasados como parámetros
        cursor.execute("""
            SELECT 
                MIN(rechazadas) AS min_rechazadas,
                MAX(rechazadas) AS max_rechazadas,
                MIN(molde_macho) AS min_molde_macho,
                MAX(molde_macho) AS max_molde_macho,
                MIN(molde_hembra) AS min_molde_hembra,
                MAX(molde_hembra) AS max_molde_hembra,
                MIN(c_producto) AS min_c_producto,
                MAX(c_producto) AS max_c_producto,
                MIN(zona_1) AS min_zona_1,
                MAX(zona_1) AS max_zona_1,
                MIN(zona_2) AS min_zona_2,
                MAX(zona_2) AS max_zona_2,
                MIN(zona_3) AS min_zona_3,
                MAX(zona_3) AS max_zona_3,
                MIN(zona_4) AS min_zona_4,
                MAX(zona_4) AS max_zona_4,
                MIN(zona_5) AS min_zona_5,
                MAX(zona_5) AS max_zona_5
            FROM sistemaweb_produccion
            WHERE 
                cantidad_fabricada <= %s AND
                operario = %s AND
                producto = %s;
        """, [cantidad_fabricada, operario, producto])
        
        # Obtener el resultado de la consulta
        resultado = cursor.fetchone()
        
        # Crear un diccionario para facilitar el acceso a los valores
        datos_min_max = {
            'min_rechazadas': resultado[0],
            'max_rechazadas': resultado[1],
            'min_molde_macho': resultado[2],
            'max_molde_macho': resultado[3],
            'min_molde_hembra': resultado[4],
            'max_molde_hembra': resultado[5],
            'min_c_producto': resultado[6],
            'max_c_producto': resultado[7],
            'min_zona_1': resultado[8],
            'max_zona_1': resultado[9],
            'min_zona_2': resultado[10],
            'max_zona_2': resultado[11],
            'min_zona_3': resultado[12],
            'max_zona_3': resultado[13],
            'min_zona_4': resultado[14],
            'max_zona_4': resultado[15],
            'min_zona_5': resultado[16],
            'max_zona_5': resultado[17],
        }
        
        return datos_min_max
    
class Prediction94APIView(APIView):
    
    def get_label_value(self, model, id):
        """
        Función auxiliar para obtener el valor de la tabla LabelEncoderTable
        basado en el nombre del objeto relacionado.
        """
        try:
            instance = model.objects.get(id=id)
            nombre = f"{instance.first_name} {instance.last_name}" if model == User else instance.nombre
            valor = LabelEncoderTable.objects.get(nombre=nombre).valor
            
            # Verificar que el valor es numérico
            if not isinstance(valor, (int, float)):
                raise ValidationError({'error': f'El valor obtenido de {model.__name__} no es numérico: {valor}'})
                
            return valor
        except (model.DoesNotExist, LabelEncoderTable.DoesNotExist):
            raise ValidationError({'error': f'ID {id} o nombre no encontrado en {model.__name__} o LabelEncoderTable'})

    def post(self, request, *args, **kwargs):
        data = request.data

        # Verificar campos requeridos
        required_fields = ['Cantidad_Fabric', 'Rechaz_No_Ok', 'Extra_Ok', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 
                           'Merma_gr', 'Ciclo_seg', 'Operario', 'Responsable', 'Producto', 
                           'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
        
        missing_fields = [field for field in required_fields if field not in data or data[field] in [None, '']]
        if missing_fields:
            raise ValidationError({'error': f'Complete los siguientes campos: {missing_fields}'})

        # Verificar campos numéricos en cero
        zero_fields = ['Cantidad_Fabric', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 'Merma_gr', 'Ciclo_seg']
        if any(float(data[field]) < 1 for field in zero_fields):
            return Response({'prediction': 0}, status=status.HTTP_200_OK)
        
        # Diccionario de verificación de rangos
        ranges = {
             'Cantidad_Fabric':(200,600),'Largo': (10, 60), 'Ancho': (1, 8),'Merma_gr': (1, 5),'Ciclo_seg':(8,200)
         }
        #8-848

         # Verificar rangos
        for field, (min_val, max_val) in ranges.items():
             if not (min_val <= float(data[field]) <= max_val):
                 print(field)
                 return Response({'prediction': 0}, status=status.HTTP_200_OK)

        # Obtener el operario por el ID proporcionado y concatenar nombre y apellido
        try:
            operario = User.objects.get(id=data['Operario'])
            operario_nombre_completo = f"{operario.first_name} {operario.last_name}"
        except User.DoesNotExist:
            raise ValidationError({'error': 'Operario no encontrado.'})

        # Obtener el nombre del producto por su ID
        try:
            producto = Producto.objects.get(id=data['Producto'])
            producto_nombre = producto.nombre  # Suponiendo que la columna nombre existe en la tabla Producto
        except Producto.DoesNotExist:
            raise ValidationError({'error': 'Producto no encontrado.'})


        
        # Obtener los valores mínimos y máximos
        resultado = obtener_valores_min_max(data['Cantidad_Fabric'], operario_nombre_completo, producto_nombre)

        # Lista para almacenar los resultados de las simulaciones
        simulation_results = []
        label_fields = ['Operario', 'Responsable', 'Producto', 'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
        label_models = [User, User, Producto, TipoProducto, MateriaPrima, MateriaPrima, MateriaPrima, MaquinaInyeccion, Turno]
        label_values = [int(self.get_label_value(model, data[field])) for field, model in zip(label_fields, label_models)]
        # Realizar 10 iteraciones
        for i in range(10):
            # Simular valores aleatorios para los campos de temperatura y molde si no se encuentran o están en 0
            simulated_values = {
                'Rechaz_No_Ok':int((resultado['min_rechazadas'] + resultado['max_rechazadas'])/2),  
                'C_Molde_Macho': random.randint(resultado['min_molde_macho'], resultado['max_molde_macho']), 
                'C_Molde_Hembra': random.randint(resultado['min_molde_hembra'], resultado['max_molde_hembra']),  
                'C_Product': random.randint(resultado['min_c_producto'], resultado['max_c_producto']),  
                'Zona_1': random.randint(resultado['min_zona_1'], resultado['max_zona_1']),  
                'Zona_2': random.randint(resultado['min_zona_2'], resultado['max_zona_2']),  
                'Zona_3': random.randint(resultado['min_zona_3'], resultado['max_zona_3']), 
                'Zona_4': random.randint(resultado['min_zona_4'], resultado['max_zona_4']),  
                'Zona_5': random.randint(resultado['min_zona_5'], resultado['max_zona_5']),  
            }

            # Obtener los valores de las tablas correspondientes
           

            # Asegurarse de que los datos se envían en el orden correcto
            input_data = [
                data['Cantidad_Fabric'],  # Cantidad_Fabric
                simulated_values['Rechaz_No_Ok'],   # Rechaz_No_Ok
                data['Extra_Ok'],  # Extra_Ok
                data['Largo'],  # Largo
                data['Ancho'],  # Ancho
                data['MP_KG'],  # MP_KG
                data['Aditi_KG'],  # Aditi_KG
                data['Merma_gr'],  # Merma_gr
                data['Ciclo_seg'],  # Ciclo_seg
                simulated_values['C_Molde_Macho'],  # C_Molde_Macho
                simulated_values['C_Molde_Hembra'],  # C_Molde_Hembra
                simulated_values['C_Product'],  # C_Product
                600,  # Peso_gr_prensad
                simulated_values['Zona_1'],  # Zona_1
                simulated_values['Zona_2'],  # Zona_2
                simulated_values['Zona_3'],  # Zona_3
                simulated_values['Zona_4'],  # Zona_4
                simulated_values['Zona_5'],  # Zona_5
                label_values[0],  # operario
                label_values[1],
                label_values[2],  # resposable
                label_values[3],  # Tipo
                label_values[4],  # Color
                label_values[5],  # MP_Cod
                label_values[6],  # Aditivo
                label_values[7],  # Nombre de la Máquina
                label_values[8]  # Turno
            ]

           
            input_values = np.array(input_data, dtype=float).reshape(1, -1)
            print(input_values)
            # Realizar la predicción usando el modelo
            prediction = modelo.predict(input_values)
            rounded_prediction = np.round(prediction, decimals=1)

            # Guardar los resultados de la simulación
            simulation_results.append({
                'input_data': input_data,  # Asegúrate de que el array sea serializable
                'prediction': rounded_prediction[0][0]  # Predicción redondeada
            })
            simulation_results = sorted(simulation_results, key=lambda x: x['prediction'])
        # Devolver los resultados de las 10 simulaciones
        return Response(simulation_results, status=status.HTTP_200_OK)

# class Prediction94APIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         # Verificar campos requeridos
#         required_fields = ['Cantidad_Fabric', 'Rechaz_No_Ok', 'Extra_Ok', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 
#                            'Merma_gr', 'Ciclo_seg', 'C_Molde_Macho', 'C_Molde_Hembra', 'C_Product', 'Peso_gr_prensad', 
#                            'Zona_1', 'Zona_2', 'Zona_3', 'Zona_4', 'Zona_5', 'Operario', 'Responsable', 'Producto', 
#                            'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
#         missing_fields = [field for field in required_fields if field not in data or data[field] in [None, '']]
#         if missing_fields:
#             raise ValidationError({'error': f'Complete los siguientes campos: {missing_fields}'})

#         # Verificar campos numéricos en cero
#         zero_fields = ['Cantidad_Fabric', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 'Merma_gr', 'Ciclo_seg', 
#                        'C_Molde_Macho', 'C_Molde_Hembra', 'C_Product', 'Peso_gr_prensad', 'Zona_1', 'Zona_2', 
#                        'Zona_3', 'Zona_4', 'Zona_5']
#         if any(float(data[field]) < 0.5 for field in zero_fields):
#             return Response({'prediction': 0}, status=status.HTTP_200_OK)

#         # Diccionario de verificación de rangos
#         ranges = {
#             'Aditi_KG': (1, 7), 'Largo': (40, 600), 'Ancho': (5, 69), 'MP_KG': (0.5, 65), 'Merma_gr': (1, 5),
#             'Ciclo_seg': (8, 300), 'Peso_gr_prensad': (8, 845), 'C_Molde_Macho': (18, 50), 'C_Molde_Hembra': (18, 50),
#             'C_Product': (18, 75), 'Zona_1': (60, 260), 'Zona_2': (160, 260), 'Zona_3': (160, 260), 
#             'Zona_4': (175, 240), 'Zona_5': (1, 230)
#         }

#         # Verificar rangos
#         for field, (min_val, max_val) in ranges.items():
#             if not (min_val <= float(data[field]) <= max_val):
#                 print(field)
#                 return Response({'prediction': 0}, status=status.HTTP_200_OK)

#         # Función auxiliar para obtener el valor de la tabla LabelEncoderTable
#         def get_label_value(model, id):
#             try:
#                 instance = model.objects.get(id=id)
#                 nombre = f"{instance.first_name} {instance.last_name}" if model == User else instance.nombre
#                 return LabelEncoderTable.objects.get(nombre=nombre).valor
#             except (model.DoesNotExist, LabelEncoderTable.DoesNotExist):
#                 raise ValidationError({'error': f'ID {id} o nombre no encontrado en {model.__name__} o LabelEncoderTable'})

#         # Obtener los valores de las tablas correspondientes
#         label_fields = ['Operario', 'Responsable', 'Producto', 'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
#         label_models = [User, User, Producto, TipoProducto, MateriaPrima, MateriaPrima, MateriaPrima, MaquinaInyeccion, Turno]
#         label_values = [float(get_label_value(model, data[field])) for field, model in zip(label_fields, label_models)]

#         # Convertir los datos de entrada en un array numpy
#         input_data = np.array([
#             float(data['Cantidad_Fabric']), float(data['Rechaz_No_Ok']), float(data['Extra_Ok']), float(data['Largo']),
#             float(data['Ancho']), float(data['MP_KG']), float(data['Aditi_KG']), float(data['Merma_gr']), float(data['Ciclo_seg']),
#             float(data['C_Molde_Macho']), float(data['C_Molde_Hembra']), float(data['C_Product']), float(data['Peso_gr_prensad']),
#             float(data['Zona_1']), float(data['Zona_2']), float(data['Zona_3']), float(data['Zona_4']), float(data['Zona_5'])
#         ] + label_values).reshape(1, -1)  # Asegura que sea una matriz 2D

#         # Realizar la predicción
#         print(input_data)
#         try:
#             prediction = modelo.predict(input_data)
#             rounded_prediction = np.round(prediction, decimals=1)
#             return Response({'prediction': rounded_prediction[0][0]}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecomendacionAPIView(APIView):

    def get_label_value(self, model, id):
        """
        Función auxiliar para obtener el valor de la tabla LabelEncoderTable
        basado en el nombre del objeto relacionado.
        """
        try:
            instance = model.objects.get(id=id)
            nombre = f"{instance.first_name} {instance.last_name}" if model == User else instance.nombre
            valor = LabelEncoderTable.objects.get(nombre=nombre).valor

            # Verificar que el valor es numérico
            if not isinstance(valor, (int, float)):
                raise ValidationError({'error': f'El valor obtenido de {model.__name__} no es numérico: {valor}'})

            return valor
        except (model.DoesNotExist, LabelEncoderTable.DoesNotExist):
            raise ValidationError({'error': f'ID {id} o nombre no encontrado en {model.__name__} o LabelEncoderTable'})

    def post(self, request, *args, **kwargs):
        data = request.data

        # Validar campos requeridos
        required_fields = ['Cantidad_Fabric', 'Rechaz_No_Ok', 'Extra_Ok', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG',
                           'Merma_gr', 'Ciclo_seg', 'Operario', 'Responsable', 'Producto',
                           'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno', 'min_prediction']
        missing_fields = [field for field in required_fields if field not in data or data[field] in [None, '']]
        if missing_fields:
            raise ValidationError({'error': f'Complete los siguientes campos: {missing_fields}'})

        # Obtener el valor mínimo de predicción aceptable
        min_prediction = float(data['min_prediction'])

        # Verificar campos numéricos en cero o negativos
        zero_fields = ['Cantidad_Fabric', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 'Merma_gr']
        if any(float(data[field]) < 0.5 for field in zero_fields):
            return Response({'error': 'Algunos campos tienen valores inválidos (cero o negativos).'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            operario = User.objects.get(id=data['Operario'])
            operario_nombre_completo = f"{operario.first_name} {operario.last_name}"
        except User.DoesNotExist:
            raise ValidationError({'error': 'Operario no encontrado.'})

        # Obtener el nombre del producto por su ID
        try:
            producto = Producto.objects.get(id=data['Producto'])
            producto_nombre = producto.nombre  # Suponiendo que la columna nombre existe en la tabla Producto
        except Producto.DoesNotExist:
            raise ValidationError({'error': 'Producto no encontrado.'})

        # Obtener los valores mínimos y máximos
        resultado = obtener_valores_min_max(data['Cantidad_Fabric'], operario_nombre_completo, producto_nombre)
        label_fields = ['Operario', 'Responsable', 'Producto', 'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
        label_models = [User, User, Producto, TipoProducto, MateriaPrima, MateriaPrima, MateriaPrima, MaquinaInyeccion, Turno]
        label_values = [int(self.get_label_value(model, data[field])) for field, model in zip(label_fields, label_models)]

        ranges = {
            'C_Molde_Macho': (resultado['min_molde_macho'], resultado['max_molde_macho']),
            'C_Molde_Hembra': (resultado['min_molde_hembra'], resultado['max_molde_hembra']),
            'C_Product': (resultado['min_c_producto'], resultado['max_c_producto']),
            'Zona_1': (resultado['min_zona_1'], resultado['max_zona_1']),
            'Zona_2': (resultado['min_zona_2'], resultado['max_zona_2']),
            'Zona_3': (resultado['min_zona_3'], resultado['max_zona_3']),
            'Zona_4': (resultado['min_zona_4'], resultado['max_zona_4']),
            'Zona_5': (resultado['min_zona_5'], resultado['max_zona_5'])
        }

        simulated_values = {
            'Rechaz_No_Ok': int((resultado['min_rechazadas'] + resultado['max_rechazadas']) / 2),
            'C_Molde_Macho': int((resultado['min_molde_macho'] + resultado['max_molde_macho']) / 2),
            'C_Molde_Hembra': int((resultado['min_molde_hembra'] + resultado['max_molde_hembra']) / 2),
            'C_Product': int((resultado['min_c_producto'] + resultado['max_c_producto']) / 2),
            'Zona_1': int((resultado['min_zona_1'] + resultado['max_zona_1']) / 2),
            'Zona_2': int((resultado['min_zona_2'] + resultado['max_zona_2']) / 2),
            'Zona_3': int((resultado['min_zona_3'] + resultado['max_zona_3']) / 2),
            'Zona_4': int((resultado['min_zona_4'] + resultado['max_zona_4']) / 2),
            'Zona_5': int((resultado['min_zona_5'] + resultado['max_zona_5']) / 2),
        }

        # Construcción de input_data con los valores simulados
        input_data = [
            data['Cantidad_Fabric'],  # Cantidad_Fabric (sin optimización)
            simulated_values['Rechaz_No_Ok'],   # Rechaz_No_Ok (sin optimización)
            data['Extra_Ok'],  # Extra_Ok (sin optimización)
            data['Largo'],  # Largo (sin optimización)
            data['Ancho'],  # Ancho (sin optimización)
            data['MP_KG'],  # MP_KG (sin optimización)
            data['Aditi_KG'],  # Aditi_KG (sin optimización)
            data['Merma_gr'],  # Merma_gr (sin optimización)
            data['Ciclo_seg'],  # Ciclo_seg (sin optimización)
            simulated_values['C_Molde_Macho'],  # C_Molde_Macho (optimizable)
            simulated_values['C_Molde_Hembra'],  # C_Molde_Hembra (optimizable)
            simulated_values['C_Product'],  # C_Product (optimizable)
            200,  # Peso_gr_prensad (sin optimización)
            simulated_values['Zona_1'],  # Zona_1 (optimizable)
            simulated_values['Zona_2'],  # Zona_2 (optimizable)
            simulated_values['Zona_3'],  # Zona_3 (optimizable)
            simulated_values['Zona_4'],  # Zona_4 (optimizable)
            simulated_values['Zona_5'],  # Zona_5 (optimizable)
            label_values[0],  # Operario (a optimizar)
            label_values[1],  # Responsable (a optimizar)
            label_values[2],  # Producto (sin optimización)
            label_values[3],  # Tipo (sin optimización)
            label_values[4],  # Color (sin optimización)
            label_values[5],  # MP_Cod (sin optimización)
            label_values[6],  # Aditivo (sin optimización)
            label_values[7],  # Maquina (a optimizar)
            label_values[8]   # Turno (sin optimización)
        ]

        input_values = np.array(input_data, dtype=float).reshape(1, -1)

        # Pasar input_values al método de optimización
        optimal_data, valid = self.optimize_data_for_prediction(input_values, ranges, min_prediction)

        # Ahora optimizamos Operario, Responsable y Maquina
        best_operario_value = None
        best_responsable_value = None
        best_maquina_value = None
        best_prediction = None
        best_optimal_data = None

        # Índices en optimal_data
        operario_index = 18
        responsable_index = 19
        maquina_index = 25

        # Probar valores de Operario de 0 a 6
        for operario_value in range(0, 7):
            # Probar valores de Responsable de 0 a 2
            for responsable_value in range(0, 3):
                # Probar valores de Maquina de 0 a 3
                for maquina_value in range(0, 4):
                    # Crear una copia de optimal_data para no modificar el original
                    temp_optimal_data = optimal_data.copy()
                    temp_optimal_data[0][operario_index] = operario_value
                    temp_optimal_data[0][responsable_index] = responsable_value
                    temp_optimal_data[0][maquina_index] = maquina_value

                    # Realizar la predicción
                    prediction = modelo.predict(temp_optimal_data)[0]

                    # Agregar prints para ver la evaluación
                    print(f"Probando Operario valor: {operario_value}, Responsable valor: {responsable_value}, Maquina valor: {maquina_value}, Predicción: {prediction}")

                    # Verificar si la predicción cumple las condiciones
                    if prediction <= 100:
                        if best_prediction is None or prediction > best_prediction:
                            best_prediction = prediction
                            best_operario_value = operario_value
                            best_responsable_value = responsable_value
                            best_maquina_value = maquina_value
                            best_optimal_data = temp_optimal_data.copy()
                            print(f"--> Nueva mejor predicción encontrada: {best_prediction} con Operario: {operario_value}, Responsable: {responsable_value}, Maquina: {maquina_value}")

        if best_operario_value is None or best_responsable_value is None or best_maquina_value is None:
            return Response({'error': 'No se encontraron valores para recomendar'}, status=status.HTTP_400_BAD_REQUEST)

        # Reemplazar los valores en optimal_data con los mejores valores encontrados
        optimal_data = best_optimal_data
        optimized_prediction = best_prediction

        # Obtener los nombres correspondientes a los mejores valores
        try:
            best_operario_nombre = LabelEncoderTable.objects.get(valor=best_operario_value, categoria='operario').nombre
        except LabelEncoderTable.DoesNotExist:
            best_operario_nombre = f"Operario con valor {best_operario_value}"

        try:
            best_responsable_nombre = LabelEncoderTable.objects.get(valor=best_responsable_value, categoria='responsable').nombre
        except LabelEncoderTable.DoesNotExist:
            best_responsable_nombre = f"Responsable con valor {best_responsable_value}"

        try:
            best_maquina_nombre = LabelEncoderTable.objects.get(valor=best_maquina_value, categoria='maquina').nombre
        except LabelEncoderTable.DoesNotExist:
            best_maquina_nombre = f"Maquina con valor {best_maquina_value}"

        # Preparar la respuesta
        field_names = [
            'Cantidad_Fabric', 'Rechaz_No_Ok', 'Extra_Ok', 'Largo', 'Ancho', 'MP_KG',
            'Aditi_KG', 'Merma_gr', 'Ciclo_seg', 'C_Molde_Macho', 'C_Molde_Hembra',
            'C_Product', 'Peso_gr_prensad', 'Zona_1', 'Zona_2', 'Zona_3', 'Zona_4',
            'Zona_5', 'Operario', 'Responsable', 'Producto', 'Tipo', 'Color', 'MP_Cod',
            'Aditivo', 'Maquina', 'Turno'
        ]

        optimal_data_dict = dict(zip(field_names, optimal_data[0]))

        # Reemplazar los valores codificados por los nombres
        optimal_data_dict['Operario'] = best_operario_nombre
        optimal_data_dict['Responsable'] = best_responsable_nombre
        optimal_data_dict['Maquina'] = best_maquina_nombre

        # Preparar la respuesta
        response_data = {
            'optimal_data': optimal_data_dict,
            'prediction': float(optimized_prediction)
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def optimize_data_for_prediction(self, input_values, ranges, min_prediction):
        """Optimiza solo los campos especificados en 'ranges' dentro de los rangos para mejorar la predicción sin superar el valor de 100."""
        optimal_data = input_values.copy()
        field_indices = {
            'C_Molde_Macho': 9,
            'C_Molde_Hembra': 10,
            'C_Product': 11,
            'Zona_1': 13,
            'Zona_2': 14,
            'Zona_3': 15,
            'Zona_4': 16,
            'Zona_5': 17
        }
        # Optimizar solo los campos especificados en el diccionario de rangos
        for field, (min_val, max_val) in ranges.items():
            i = field_indices[field]
            current_value = float(input_values[0][i])

            # Calcular el promedio entre el valor actual y los límites del rango
            average_min = (min_val + current_value) / 2
            average_max = (max_val + current_value) / 2

            # Empezamos con el valor actual como óptimo
            optimal_value = current_value

            # Evaluar predicciones con valores modificados
            for value in [average_min, average_max]:
                optimal_data[0][i] = value
                prediction = modelo.predict(optimal_data)[0]
                print(f"Optimización de {field}: probando valor {value}, predicción {prediction}")

                # Validar que la predicción esté en el rango deseado
                if prediction <= 100:
                    optimal_value = value

            # Asignar el valor óptimo al campo
            optimal_data[0][i] = optimal_value
            print(f"Valor óptimo para {field}: {optimal_value}")

        # Verificar que la predicción final esté dentro de los límites
        final_prediction = modelo.predict(optimal_data)[0]
        if final_prediction < min_prediction or final_prediction > 100:
            return optimal_data, False

        return optimal_data, True



# class RecomendacionAPIView(APIView):
    
#     def get_label_value(self, model, id):
#         """
#         Función auxiliar para obtener el valor de la tabla LabelEncoderTable
#         basado en el nombre del objeto relacionado.
#         """
#         try:
#             instance = model.objects.get(id=id)
#             nombre = f"{instance.first_name} {instance.last_name}" if model == User else instance.nombre
#             valor = LabelEncoderTable.objects.get(nombre=nombre).valor
            
#             # Verificar que el valor es numérico
#             if not isinstance(valor, (int, float)):
#                 raise ValidationError({'error': f'El valor obtenido de {model.__name__} no es numérico: {valor}'})
                
#             return valor
#         except (model.DoesNotExist, LabelEncoderTable.DoesNotExist):
#             raise ValidationError({'error': f'ID {id} o nombre no encontrado en {model.__name__} o LabelEncoderTable'})

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         # Verificar campos requeridos
#         required_fields = ['Cantidad_Fabric', 'Rechaz_No_Ok', 'Extra_Ok', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 
#                            'Merma_gr', 'Ciclo_seg', 'Peso_gr_prensad', 'Responsable', 'Producto', 
#                            'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
        
#         missing_fields = [field for field in required_fields if field not in data or data[field] in [None, '']]
#         if missing_fields:
#             raise ValidationError({'error': f'Complete los siguientes campos: {missing_fields}'})

#         # Verificar campos numéricos en cero
#         zero_fields = ['Cantidad_Fabric', 'Largo', 'Ancho', 'MP_KG', 'Aditi_KG', 'Merma_gr', 'Ciclo_seg', 
#                        'Peso_gr_prensad']
#         if any(float(data[field]) < 1 for field in zero_fields):
#             return Response({'prediction': 0}, status=status.HTTP_200_OK)
        
#         # Diccionario de verificación de rangos
#         ranges = {
#             'Cantidad_Fabric':(200,600), 'Largo': (10, 60), 'Ancho': (1, 8), 'Merma_gr': (1, 5), 
#             'Ciclo_seg': (8,300), 'Peso_gr_prensad': (8,120)
#         }

#         # Verificar rangos
#         for field, (min_val, max_val) in ranges.items():
#             if not (min_val <= float(data[field]) <= max_val):
#                 print(field)
#                 return Response({'prediction': 0}, status=status.HTTP_200_OK)

#       # Obtener el operario por el ID proporcionado y concatenar nombre y apellido
#         try:
#             operario = User.objects.get(id=data['Operario'])
#             operario_nombre_completo = f"{operario.first_name} {operario.last_name}"
#         except User.DoesNotExist:
#             raise ValidationError({'error': 'Operario no encontrado.'})

#         # Obtener el nombre del producto por su ID
#         try:
#             producto = Producto.objects.get(id=data['Producto'])
#             producto_nombre = producto.nombre  # Suponiendo que la columna nombre existe en la tabla Producto
#         except Producto.DoesNotExist:
#             raise ValidationError({'error': 'Producto no encontrado.'})

#         # Obtener los valores mínimos y máximos
#         resultado = obtener_valores_min_max(data['Cantidad_Fabric'], operario_nombre_completo, producto_nombre)
#         label_fields = ['Operario', 'Responsable', 'Producto', 'Tipo', 'Color', 'MP_Cod', 'Aditivo', 'Maquina', 'Turno']
#         label_models = [User, User, Producto, TipoProducto, MateriaPrima, MateriaPrima, MateriaPrima, MaquinaInyeccion, Turno]
#         label_values = [int(self.get_label_value(model, data[field])) for field, model in zip(label_fields, label_models)]
#         # Variables para almacenar el mejor operario y la mejor predicción
#         mejor_operario = None
#         mejor_maquina = None
#         mejor_ciclo = None
#         mejor_prediccion = float('-inf')  # Valor negativo muy bajo para iniciar la comparación

#         # Evaluar operarios (del 1 al 6)
#         for operario_id in range(0, 6):
#             # Simular valores aleatorios para los campos de temperatura y molde si no se encuentran o están en 0
#             simulated_values = {
#                 'Rechaz_No_Ok': int((resultado['min_rechazadas'] + resultado['max_rechazadas']) / 2),  
#                 'C_Molde_Macho': random.randint(resultado['min_molde_macho'], resultado['max_molde_macho']), 
#                 'C_Molde_Hembra': random.randint(resultado['min_molde_hembra'], resultado['max_molde_hembra']),  
#                 'C_Product': random.randint(resultado['min_c_producto'], resultado['max_c_producto']),  
#                 'Zona_1': random.randint(resultado['min_zona_1'], resultado['max_zona_1']),  
#                 'Zona_2': random.randint(resultado['min_zona_2'], resultado['max_zona_2']),  
#                 'Zona_3': random.randint(resultado['min_zona_3'], resultado['max_zona_3']), 
#                 'Zona_4': random.randint(resultado['min_zona_4'], resultado['max_zona_4']),  
#                 'Zona_5': random.randint(resultado['min_zona_5'], resultado['max_zona_5']),  
#             }

#             # Asegurarse de que los datos se envían en el orden correcto
#             input_data = [
#                 data['Cantidad_Fabric'],  # Cantidad_Fabric
#                 simulated_values['Rechaz_No_Ok'],  # Rechaz_No_Ok
#                 data['Extra_Ok'],  # Extra_Ok
#                 data['Largo'],  # Largo
#                 data['Ancho'],  # Ancho
#                 data['MP_KG'],  # MP_KG
#                 data['Aditi_KG'],  # Aditi_KG
#                 data['Merma_gr'],  # Merma_gr
#                 data['Ciclo_seg'],  # Ciclo_seg
#                 simulated_values['C_Molde_Macho'],  # C_Molde_Macho
#                 simulated_values['C_Molde_Hembra'],  # C_Molde_Hembra
#                 simulated_values['C_Product'],  # C_Product
#                 data['Peso_gr_prensad'],  # Peso_gr_prensad
#                 simulated_values['Zona_1'],  # Zona_1
#                 simulated_values['Zona_2'],  # Zona_2
#                 simulated_values['Zona_3'],  # Zona_3
#                 simulated_values['Zona_4'],  # Zona_4
#                 simulated_values['Zona_5'],  # Zona_5
#                 operario_id,  # ID del operario que estamos evaluando
#                 label_values[1],
#                 label_values[2],  # resposable
#                 label_values[3],  # Tipo
#                 label_values[4],  # Color
#                 label_values[5],  # MP_Cod
#                 label_values[6],  # Aditivo
#                 label_values[7],  # Nombre de la Máquina
#                 label_values[8]
#             ]
#             print(input_data)

#             input_values = np.array(input_data, dtype=float).reshape(1, -1)
#             prediction = modelo.predict(input_values)
#             rounded_prediction = np.round(prediction, decimals=1)

#             # Comparar la predicción actual con la mejor predicción encontrada
#             if rounded_prediction[0][0] <= 100 and rounded_prediction[0][0] > 80:
#                 mejor_prediccion = rounded_prediction[0][0]
#                 mejor_operario = operario_id

        
#         for maquina_id in range(0, 4):
#             # Simular valores aleatorios para los campos de temperatura y molde si no se encuentran o están en 0
#             simulated_values = {
#                 'Rechaz_No_Ok': int((resultado['min_rechazadas'] + resultado['max_rechazadas']) / 2),  
#                 'C_Molde_Macho': random.randint(resultado['min_molde_macho'], resultado['max_molde_macho']), 
#                 'C_Molde_Hembra': random.randint(resultado['min_molde_hembra'], resultado['max_molde_hembra']),  
#                 'C_Product': random.randint(resultado['min_c_producto'], resultado['max_c_producto']),  
#                 'Zona_1': random.randint(resultado['min_zona_1'], resultado['max_zona_1']),  
#                 'Zona_2': random.randint(resultado['min_zona_2'], resultado['max_zona_2']),  
#                 'Zona_3': random.randint(resultado['min_zona_3'], resultado['max_zona_3']), 
#                 'Zona_4': random.randint(resultado['min_zona_4'], resultado['max_zona_4']),  
#                 'Zona_5': random.randint(resultado['min_zona_5'], resultado['max_zona_5']),  
#             }

#             # Asegurarse de que los datos se envían en el orden correcto
#             input_data = [
#                 data['Cantidad_Fabric'],  # Cantidad_Fabric
#                 simulated_values['Rechaz_No_Ok'],  # Rechaz_No_Ok
#                 data['Extra_Ok'],  # Extra_Ok
#                 data['Largo'],  # Largo
#                 data['Ancho'],  # Ancho
#                 data['MP_KG'],  # MP_KG
#                 data['Aditi_KG'],  # Aditi_KG
#                 data['Merma_gr'],  # Merma_gr
#                 data['Ciclo_seg'],  # Ciclo_seg
#                 simulated_values['C_Molde_Macho'],  # C_Molde_Macho
#                 simulated_values['C_Molde_Hembra'],  # C_Molde_Hembra
#                 simulated_values['C_Product'],  # C_Product
#                 data['Peso_gr_prensad'],  # Peso_gr_prensad
#                 simulated_values['Zona_1'],  # Zona_1
#                 simulated_values['Zona_2'],  # Zona_2
#                 simulated_values['Zona_3'],  # Zona_3
#                 simulated_values['Zona_4'],  # Zona_4
#                 simulated_values['Zona_5'],  # Zona_5
#                 mejor_operario,  # ID del operario que estamos evaluando
#                 label_values[1],
#                 label_values[2],  # resposable
#                 label_values[3],  # Tipo
#                 label_values[4],  # Color
#                 label_values[5],  # MP_Cod
#                 label_values[6],  # Aditivo
#                 maquina_id,  # Nombre de la Máquina
#                 label_values[8]
#             ]
           

#             input_values = np.array(input_data, dtype=float).reshape(1, -1)
#             prediction = modelo.predict(input_values)
#             rounded_prediction = np.round(prediction, decimals=1)

#             # Comparar la predicción actual con la mejor predicción encontrada
#             if rounded_prediction[0][0] <= 100 and rounded_prediction[0][0] > 80:
#                 print(input_data)
#                 mejor_prediccion = rounded_prediction[0][0]
#                 mejor_maquina = maquina_id

#             # Simular valores aleatorios para los campos de temperatura y molde si no se encuentran o están en 0
#             # Calcular los valores medios para el ciclo (Ciclo_seg)
#             ciclo_1 = (float(data['Ciclo_seg']) + 300) / 2  # Promedio de 180 y 300
#             ciclo_2 = (float(data['Ciclo_seg']) + 8) / 2    # Promedio de 180 y 8


#         # Devolver el mejor operario y la mejor predicción
#         print(mejor_operario, mejor_maquina,ciclo_2,ciclo_1 )

#         try:
#             # Buscar el operario en LabelEncoderTable usando el valor y la categoría "Operador"
#             operario = LabelEncoderTable.objects.get(valor=mejor_operario, categoria="Operario")
            
#             # Asumiendo que el nombre del operario está en el campo `nombre`
#             operario_nombre_completo_f = operario.nombre  # Puedes modificar este campo si el nombre está almacenado de otra forma
#         except LabelEncoderTable.DoesNotExist:
#             raise ValidationError({'error': 'Operario no encontrado en la categoría Operador.'})

#         # Obtener el nombre de la máquina por su ID
#         try:
#             maquina = MaquinaInyeccion.objects.get(id=mejor_maquina)
#             maquina_nombre = maquina.nombre  # Suponiendo que la columna nombre existe en la tabla MaquinaInyeccion
#         except MaquinaInyeccion.DoesNotExist:
#             raise ValidationError({'error': 'Máquina no encontrada.'})

#         return Response({
#             'mejor_operario': operario_nombre_completo_f,
#             'mejor_maquina': maquina_nombre,
#             'Ciclo_min':ciclo_2,
#             'Ciclo_max':ciclo_1,
#         }, status=status.HTTP_200_OK)