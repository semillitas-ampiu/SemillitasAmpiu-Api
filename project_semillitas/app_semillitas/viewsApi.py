from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .views import *
import threading
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

#Get y Post para el admin
class AdminList(generics.ListCreateAPIView):
    queryset = Usuario.objects.filter(rol='Admin')
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            
            passwordGenerado = generar_password()
            admin= serializer.instance
            admin.set_password(passwordGenerado)
            admin.is_active = True
            admin.save()

            asunto = "Registro de Usuario en el Sistema"
            mensajeCorreo = f"""
            Cordial Saludo <b>{admin.first_name} {admin.last_name}</b>, usted ha sido registrado
            en el sistema de Gestión Administradores de Semillitas Ampiu Sena.
            <br><br>nos permtimos enviar las credenciales de ingreso al sistema<br><br>
            <b>Username:</b> {admin.username}<br>
            <b>Password:</b> {passwordGenerado}<br>
            La URL del sistema es: http://localhost:5173/"""
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [admin.email], None)
            )
            thread.start()
            return Response(
                {'mensaje':'Administrador creado correctamente','data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'mensaje':'Error al crear el Administrador','errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
#Update y delete admin
class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.filter(rol='Admin')
    serializer_class = AdminSerializer

#Get y Post Jugador
class JugadorList(generics.ListCreateAPIView):
    queryset = queryset = Usuario.objects.filter(rol='Jugador')
    serializer_class =JugadorSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            
            self.perform_create(serializer)
            
            return Response(
                {'mensaje':'Jugador creado correctamente','data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'mensaje':'Error al crear el Jugador','errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

#Put y Delete Jugador
class JugadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = queryset = Usuario.objects.filter(rol='Jugador')
    serializer_class = JugadorSerializer
    

class NivelList(generics.ListAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Nivel creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
class NivelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer


class EvaluacionList(generics.ListCreateAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Evaluación creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
class EvaluacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer

class PalabraList(generics.ListCreateAPIView):
    queryset = Palabra.objects.all()
    serializer_class = PalabraSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Palabra creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
      

class PalabraDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Palabra.objects.all()
    serializer_class = PalabraSerializer

class EjercicioList(generics.ListCreateAPIView):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Ejercicio creado correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

class EjercicioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

class UsuarioPalabrasList(generics.ListCreateAPIView):
    queryset = UsuarioPalabras.objects.all()
    serializer_class = UsuarioPalabrasSerializer
    permission_classes = [AllowAny] 
    filter_backends = [DjangoFilterBackend] # Usar el backend de filtro
    # Define qué campos se pueden usar para filtrar en la URL
    filterset_fields = ['usuario', 'palabra']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'UsuarioPalabras creado correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

class UsuarioPalabrasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UsuarioPalabras.objects.all()
    serializer_class = UsuarioPalabrasSerializer

class EvaluacionUsuariosList(generics.ListCreateAPIView):
    queryset = EvaluacionUsuarios.objects.all()
    serializer_class = EvaluacionUsuariosSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'EvaluacionUsuarios creado correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

class EvaluacionUsuariosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EvaluacionUsuarios.objects.all()
    serializer_class = EvaluacionUsuariosSerializer

class ResultadoEvaluacionesList(generics.ListCreateAPIView):
    queryset = ResultadoEvaluaciones.objects.all()
    serializer_class = ResultadoEvaluacionesSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'ResultadoEvaluaciones creado correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

class ResultadoEvaluacionesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResultadoEvaluaciones.objects.all()
    serializer_class = ResultadoEvaluacionesSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    