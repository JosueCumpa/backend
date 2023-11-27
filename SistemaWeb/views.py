from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from . serializers import UserSerializer, MaquinaSerializer
from .models import MaquinaInyeccion
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

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
                },
                "tokens": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )


class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = MaquinaInyeccion.objects.all()
    serializer_class = MaquinaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    