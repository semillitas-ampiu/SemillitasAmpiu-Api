from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .views import *
import threading
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend


# Get y Post para el admin
class AdminList(generics.ListCreateAPIView):
    queryset = Usuario.objects.filter(rol="Admin")
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            passwordGenerado = generar_password()
            admin = serializer.instance
            admin.set_password(passwordGenerado)
            admin.is_active = True
            admin.save()

            asunto = "Registro de Usuario en el Sistema"
            mensajeCorreo = f"""Cordial Saludo <b>{admin.first_name} {admin.last_name}</b>, usted ha sido registrado en el sistema de Gestión Administradores de Semillitas Ampiu Sena.<br><br>
Nos permitimos enviar las credenciales de ingreso al sistema:<br><br>
<b>Username:</b> {admin.username}<br>
<b>Password:</b> {passwordGenerado}<br><br>
La URL del sistema es: <a href="https://glistening-druid-395662.netlify.app/">https://semillitas-ampiu.netlify.app/</a>"""
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, admin.email, None)
            )
            thread.start()
            return Response(
                {
                    "mensaje": "Administrador creado correctamente",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "mensaje": "Error al crear el Administrador",
                    "errores": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# Update y delete admin
class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.filter(rol="Admin")
    serializer_class = AdminSerializer


# Get y Post Jugador
class JugadorList(generics.ListCreateAPIView):
    queryset = queryset = Usuario.objects.filter(rol="Jugador")
    serializer_class = JugadorSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            self.perform_create(serializer)

            return Response(
                {"mensaje": "Jugador creado correctamente", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"mensaje": "Error al crear el Jugador", "errores": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Put y Delete Jugador
class JugadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = queryset = Usuario.objects.filter(rol="Jugador")
    serializer_class = JugadorSerializer


class PalabraList(generics.ListCreateAPIView):
    queryset = Palabra.objects.all()
    serializer_class = PalabraSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"mensaje": "Palabra creada correctamente.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class PalabraDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Palabra.objects.all()
    serializer_class = PalabraSerializer


class UsuarioPalabrasList(generics.ListCreateAPIView):
    queryset = UsuarioPalabras.objects.all()
    serializer_class = UsuarioPalabrasSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]  # Usar el backend de filtro
    # Define qué campos se pueden usar para filtrar en la URL
    filterset_fields = ["usuario", "palabra"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"mensaje": "Recoleccion creado correctamente.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class UsuarioPalabrasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UsuarioPalabras.objects.all()
    serializer_class = UsuarioPalabrasSerializer


class ResultadoEvaluacionesList(generics.ListCreateAPIView):
    queryset = ResultadoEvaluaciones.objects.all()
    serializer_class = ResultadoEvaluacionesSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["usuario"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"mensaje": "Resultado creado correctamente.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class ResultadoEvaluacionesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResultadoEvaluaciones.objects.all()
    serializer_class = ResultadoEvaluacionesSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
