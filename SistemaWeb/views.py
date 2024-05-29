from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from . serializers import UserSerializer, MaquinaSerializer,TipoProductoSerializer, ProductoSerializer, CategoriaSerializer,TurnoSerializer, MateriaPrimaSerializer
from .models import MaquinaInyeccion,TipoProducto, Producto, Categoria, MateriaPrima, Turno
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import api_view

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