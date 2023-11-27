from django.urls import path, include
from . views import  UserViewSet, MaquinaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"Maquina", MaquinaViewSet, basename="MaquinasInyeccion")



urlpatterns = [ 
    path("", include(router.urls)),
]