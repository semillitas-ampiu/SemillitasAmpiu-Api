from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from .models import *
from django.db import transaction


class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'
    def create(self, validated_data):
        nivel = Nivel.objects.create(**validated_data)
        return nivel

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'
    def create(self, validated_data):
        evaluacion = Evaluacion.objects.create(**validated_data)
        return evaluacion

class PalabraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palabra
        fields = '__all__'
    def create(self, validated_data):
        palabra = Palabra.objects.create(**validated_data)
        return palabra

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        depth = 2
        extra_kwargs = {'password' :{'write_only': True, 'required':False},
            'first_name': {'required': False},
            'username':{'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'rol':{'required':False},
            'fecha_nacimiento': {'required': True}
        }
    def create(self,validated_data):
        user =  Usuario(**validated_data)
        password = validated_data.get('password')
        if password and password.strip():
            user.set_password(password)
        user.save()
        return user
    
class AdminSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Usuario
        fields = '__all__'
        # Se agregan extra_kwargs para hacer email requerido y password/username de solo lectura
        extra_kwargs = {
             'password': {'write_only': True, 'required': False},
             'username': {'required': False},
             'email': {'required': True},
             'rol': {'required': False, 'read_only': True},
             'fecha_nacimiento': {'required': True}
        }
    
    # Nuevo método para manipular los datos ANTES de llamar a .create()
    def validate(self, data):
        username = data.get('email')
        
        # Lógica: el correo es obligatorio y será el username
        if not username:
            raise serializers.ValidationError({"email": "El correo es obligatorio para el Administrador."})
            
        data['username'] = username
        data['rol'] = 'Admin'
        
        # El password se deja fuera de 'data' o con un valor nulo.
        # En este caso, no se incluye el password generado aquí, lo hará la vista.
        
        return data

    def create(self, validated_data):
        # La vista 'AdminList' se encarga de generar la contraseña y hashearla DESPUÉS de la creación.
        # Aquí solo creamos el usuario con los datos validados (que ya incluyen 'username' y 'rol').
        user = Usuario.objects.create(**validated_data)
        
        # NOTA: La contraseña no se setea aquí para que la vista pueda usar 'passwordGenerado'
        # para el correo. La vista se encarga de user.set_password() y user.save().
        
        return user
class JugadorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Usuario
        fields = '__all__'
        # Se agrega username como requerido y rol de solo lectura.
        extra_kwargs = {
             'password': {'write_only': True, 'required': False},
             'username': {'required': True}, # Username obligatorio para Jugador
             'email': {'required': False},
             'rol': {'required': False, 'read_only': True},
             'fecha_nacimiento': {'required': True}
        }
        
    def validate(self, data):
        jugador_nombre = data.get('username')
        
        if not jugador_nombre:
            raise serializers.ValidationError({"username": "El nombre de usuario es obligatorio para el Jugador."})
            
        # Lógica: si no se da password, se usa el username
        if 'password' not in data or not data['password']:
            data['password'] = jugador_nombre
            
        data['rol'] = 'Jugador'
        
        return data
        
    def create(self,validated_data):
        # 1. Creamos la instancia, la contraseña ya viene en validated_data (sea la enviada o el username)
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        
        # 2. Hasheamos la contraseña y guardamos
        if password:
            user.set_password(password)
            
        user.save()
        return user
class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'
    def create(self, validated_data):
        ejercicio = Ejercicio.objects.create(**validated_data)
        return ejercicio

class UsuarioPalabrasSerializer(serializers.ModelSerializer):
    palabra = serializers.PrimaryKeyRelatedField(
        queryset=Palabra.objects.all(),
        required=True 
    )
    palabra_data = PalabraSerializer(source='palabra', read_only=True)
    class Meta:
        model=UsuarioPalabras
        fields='__all__'
    def create(self, validated_data):       
        usuarioPalabras = UsuarioPalabras.objects.create(**validated_data)
        return usuarioPalabras
    
class EvaluacionUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionUsuarios
        fields = '__all__'
    def create(self, validated_data):
        evaluacion_usuario = EvaluacionUsuarios.objects.create(**validated_data)
        return evaluacion_usuario


class ResultadoEvaluacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoEvaluaciones
        fields = '__all__'

    def create(self, validated_data):
        resultado = ResultadoEvaluaciones.objects.create(**validated_data)
        return resultado

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user:Usuario):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        token['id'] = user.id
        token['nombre'] =  user.first_name
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Elimina las búsquedas innecesarias que causaban errores
        # admin=Usuario.objects.filter(usuario_id=self.user).first()
        
        data['user'] = {
            'id':self.user.id,
            'username':self.user.username,
            'rol':self.user.rol,
            # Se puede añadir el ID principal aquí directamente:
            'rol_id': self.user.id, 
        }
        return data