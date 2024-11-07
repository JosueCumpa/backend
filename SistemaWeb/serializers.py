from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import MaquinaInyeccion, TipoProducto, Producto, Categoria, MateriaPrima, Turno, PrediccionV2, DetallePrediccion,Recomendacion



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

            # Continuar con la creación del maquina
            MaquinaInyeccion = MaquinaInyeccion.objects.create_maquinainyeccion(**validated_data)
            return MaquinaInyeccion
        
        def update(self, instance,validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
            #Actualizar los campos relevantes del usuario
            instance.nombre = validated_data.get("nombre", instance.nombre)
            instance.estado = validated_data.get("estado", instance.estado)
            instance.save()
            return instance

class TipoProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoProducto
        fields= ['id','nombre','descripcion','estado']
    
        def create(self, validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                    raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
        
            TipoProducto = TipoProducto.objects.create_tipoproducto(**validated_data)
            return TipoProducto
    
        def update(self, instance,validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
            #Actualizar los campos relevantes
            instance.nombre = validated_data.get("nombre", instance.nombre)
            instance.estado = validated_data.get("estado", instance.estado)
            instance.save()
            return instance

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre','descripcion','estado']

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['id','nombre','estado']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ProductoSerializer(serializers.ModelSerializer):
    tipoPro_nombre = serializers.SerializerMethodField()
    class Meta:
        model= Producto
        fields=['id', 'nombre', 'descripcion', 'estado', 'tipoPro', 'tipoPro_nombre']
    
    def get_tipoPro_nombre(self, obj):
        if obj.tipoPro:
            return obj.tipoPro.nombre
        return None
    
    def validate(self, data):
        tipoPro = data.get('tipoPro')
        nombre = data.get('nombre')

        # Verificar si ya existe un producto con el mismo tipoPro y nombre, excluyendo el objeto actual en caso de actualización
        if self.instance:
            if Producto.objects.filter(tipoPro=tipoPro, nombre=nombre).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un producto con el mismo Tipo de producto y Nombre.")
        else:
            if Producto.objects.filter(tipoPro=tipoPro, nombre=nombre).exists():
                raise serializers.ValidationError("Ya existe un producto con el mismo Tipo de producto y Nombre.")
        return data
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)  #posibilidad de cambiarlo mas tarde

class MateriaPrimaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.SerializerMethodField()
    class Meta:
        model= MateriaPrima
        fields=['id', 'nombre', 'descripcion', 'estado', 'categoria', 'categoria_nombre']
    
    def get_categoria_nombre(self, obj):
        if obj.categoria:
            return obj.categoria.nombre
        return None
    
    def validate(self, data):
        categoria = data.get('categoria')
        nombre = data.get('nombre')

        # Verificar si ya existe un producto con el mismo tipoPro y nombre, excluyendo el objeto actual en caso de actualización
        if self.instance:
            if MateriaPrima.objects.filter(categoria=categoria, nombre=nombre).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Ya existe un Materia Prima con la misma Categoria y Nombre.")
        else:
            if MateriaPrima.objects.filter(categoria=categoria, nombre=nombre).exists():
                raise serializers.ValidationError("Ya existe una Materia Prima con la misma Categoria y Nombre.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class PrediccionV2Serializer(serializers.ModelSerializer):
    # Campos personalizados para mostrar los nombres de las relaciones
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    tipo_producto_nombre = serializers.CharField(source='tipo_producto.nombre', read_only=True)
    mp_cod_nombre = serializers.CharField(source='materia_prima.nombre', read_only=True)
    maquina_nombre = serializers.CharField(source='maquina.nombre', read_only=True)
    turno_nombre = serializers.CharField(source='turno.nombre', read_only=True)
    color_nombre = serializers.CharField(source='color.nombre', read_only=True)
    aditivo_nombre = serializers.CharField(source='aditivo.nombre', read_only=True)
    operario_nombre = serializers.SerializerMethodField()
    res_calidad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = PrediccionV2
        fields = [
            'id','fecha', 'cantidad', 'operario', 'operario_nombre', 'res_calidad', 'res_calidad_nombre', 
            'turno', 'turno_nombre', 'maquina', 'maquina_nombre', 'tipo_producto', 'tipo_producto_nombre', 
            'producto', 'producto_nombre', 'aditivo', 'aditivo_nombre', 'cantidad_mp', 'cantidad_aditivo', 
            'cantidad_merma', 'largo', 'ancho', 'ciclos', 'peso_prensada', 'color', 'color_nombre', 
            'materia_prima', 'mp_cod_nombre','prediccion_promedio'
        ]

    def get_operario_nombre(self, obj):
        # Concatena el first_name y last_name del operario
        operario = obj.operario
        return f"{operario.first_name} {operario.last_name}"

    def get_res_calidad_nombre(self, obj):
        # Concatena el first_name y last_name del responsable de calidad
        res_calidad = obj.res_calidad
        return f"{res_calidad.first_name} {res_calidad.last_name}"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class DetallePrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePrediccion
        fields = '__all__'

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = '__all__'
