from django.urls import path, include
from . views import  UserViewSet, MaquinaViewSet,RecomendacionViewSet,RecomendacionIDAPIView,DetallePrediccionPorIDAPIView,PrediccionV2ViewSet,DetallePrediccionViewSet,TipoProductoViewSet,TurnoViewSet,CategoriaViewSet,Prediction94APIView,RecomendacionAPIView,ListaCategoriaActivoView, ProductoViewSet, ListaTproductoActivoView, MateriaPrimaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"Maquina", MaquinaViewSet, basename="MaquinasInyeccion")
router.register(r"TipoProducto", TipoProductoViewSet, basename="TipoProducto")
router.register(r"Producto",ProductoViewSet, basename="Producto")
router.register(r'Categoria', CategoriaViewSet, basename="Categoria")
router.register(r'MateriaPrima', MateriaPrimaViewSet, basename="MateriaPrima")
router.register(r'Turno',TurnoViewSet,basename="Turno")
router.register(r"Prediccion", PrediccionV2ViewSet,basename="Prediccion")
router.register(r"DetallePrediccion", DetallePrediccionViewSet,basename="DetallePrediccion")
router.register(r"RecomendacionV2", RecomendacionViewSet, basename="RecomendacionV2")
urlpatterns = [ 
    path("", include(router.urls)),
    path("ListaTproductoActivo/",ListaTproductoActivoView.as_view(), name="ListaTproductoActivo"),
    path("ListaCategoriasActivas/", ListaCategoriaActivoView.as_view(), name="ListaCategoriasActivas"),
    path("Prediccion94/", Prediction94APIView.as_view(), name="Prediccion94"),
    path("Recomendacion/", RecomendacionAPIView.as_view(), name="Recomendacion"),
    path('Recomendacionid/<int:prediccion_id>/', RecomendacionIDAPIView.as_view(), name='Recomendacionid'),
    path('detalles-prediccion/<int:prediccion_id>/', DetallePrediccionPorIDAPIView.as_view(), name='detalles-prediccion-por-id'),
]