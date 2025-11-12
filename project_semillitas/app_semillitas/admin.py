from django.contrib import admin
from app_semillitas.models import *
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Nivel)   
admin.site.register(Palabra)
admin.site.register(Evaluacion)
admin.site.register(UsuarioPalabras)
admin.site.register(Ejercicio)
admin.site.register(EvaluacionUsuarios)
admin.site.register(ResultadoEvaluaciones)
