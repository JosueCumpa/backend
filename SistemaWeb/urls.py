from django.urls import path, include
from . views import  UserViewSet, MaquinaViewSet,TipoProductoViewSet,TurnoViewSet,CategoriaViewSet,ListaCategoriaActivoView, ProductoViewSet, ListaTproductoActivoView, MateriaPrimaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"Maquina", MaquinaViewSet, basename="MaquinasInyeccion")
router.register(r"TipoProducto", TipoProductoViewSet, basename="TipoProducto")
router.register(r"Producto",ProductoViewSet, basename="Producto")
router.register(r'Categoria', CategoriaViewSet, basename="Categoria")
router.register(r'MateriaPrima', MateriaPrimaViewSet, basename="MateriaPrima")
router.register(r'Turno',TurnoViewSet,basename="Turno")

urlpatterns = [ 
    path("", include(router.urls)),
    path("ListaTproductoActivo/",ListaTproductoActivoView.as_view(), name="ListaTproductoActivo"),
    path("ListaCategoriasActivas/", ListaCategoriaActivoView.as_view(), name="ListaCategoriasActivas")
]