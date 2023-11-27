from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MaquinaInyeccion



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "is_active", "first_name", "last_name","is_superuser","is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
            # Validar first_name y last_name antes de la creación
            #dni= validated_data["dni"]
        username = validated_data.get('username')
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        # if not dni:
        #     raise serializers.ValidationError("El campo 'dni' no puede estar vacío.")

        if not first_name:
            raise serializers.ValidationError("El campo 'first_name' no puede estar vacío.")

        if not last_name:
            raise serializers.ValidationError("El campo 'last_name' no puede estar vacío.")

        if not username:
            raise serializers.ValidationError("El campo 'username' no puede estar vacío.")

        

        # Continuar con la creación del usuario
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        
        first_name = validated_data.get("first_name", instance.first_name)
        last_name = validated_data.get("last_name", instance.last_name)

    

        if not first_name:
            raise serializers.ValidationError("El campo 'first_name' no puede estar vacío.")

        if not last_name:
            raise serializers.ValidationError("El campo 'last_name' no puede estar vacío.")

        # Actualizar los campos relevantes del usuario
        instance.username = validated_data.get("username", instance.username)
        instance.last_name = last_name
        instance.first_name = first_name
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
      
        # Establecer una nueva contraseña si se proporciona en la solicitud
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        # Guardar los cambios
        instance.save()

        return instance
    

class MaquinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaquinaInyeccion
        fields = ['id', 'nombre', 'estado']

        def create(self, validated_data):
          
            nombre = validated_data.get('nombre')

            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")

            # Continuar con la creación del usuario
            MaquinaInyeccion = MaquinaInyeccion.objects.create_maquinainyeccion(**validated_data)
            return MaquinaInyeccion


