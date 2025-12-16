from django.db import models
from django.contrib.auth.models import AbstractUser

roles = [
    ("Admin", "Admin"),
    ("Jugador", "Jugador"),
]
evaluaciones = [
    ("pares", "Pares"),
    ("union", "Union"),
]


class Usuario(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(
        blank=True, null=True, unique=True
    )  # Mantener unique para evitar duplicados
    fecha_nacimiento = models.DateField(null=False)
    rol = models.CharField(max_length=20, choices=roles)

    def __str__(self):
        return self.username


class Palabra(models.Model):
    pal_español = models.CharField(max_length=50, unique=True)
    pal_ampiu = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.pal_español


class UsuarioPalabras(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    palabra = models.ForeignKey(Palabra, on_delete=models.CASCADE)
    fecha_recogida = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "palabra")

    def __str__(self):
        return self.fecha_recogida


class ResultadoEvaluaciones(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField(default=20)
    completado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
