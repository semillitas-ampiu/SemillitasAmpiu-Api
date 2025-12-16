from django.contrib import admin
from app_semillitas.models import *
# Register your models here.

admin.site.register(Usuario)  
admin.site.register(Palabra)
admin.site.register(UsuarioPalabras)
admin.site.register(ResultadoEvaluaciones)
