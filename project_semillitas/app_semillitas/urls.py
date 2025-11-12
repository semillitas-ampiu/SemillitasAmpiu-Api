from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    #path('addEvaluacion/',viewsAdministrador.addEvaluacion,name="addEvaluacion"),
    #path('addPalabra/',viewsAdministrador.addPalabra,name="addPalabra"),
    #path('addAdmin/',viewsAdministrador.addAdmin,name="addAdmin"),
    #path('login/',views.login,name="login")
]