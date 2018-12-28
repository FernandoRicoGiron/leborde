from django.urls import path, re_path
from django.conf.urls import include
from . import views as vi

urlpatterns = [
    path('', vi.index),
    path('nosotros/', vi.nosotros),
    re_path('tienda/categoria/(?P<id>\d+)/', vi.categoria),
    re_path('tienda/coleccion/(?P<id>\d+)/', vi.coleccion),
    re_path('tienda/(?P<id>\d+)/', vi.producto),
    path('tienda/', vi.tienda),
    path('contacto/', vi.contacto),
    path('mensajecontacto/', vi.mensajecontacto),
    # Ecommerce
    path('agregarCarrito/', vi.add_to_cart),
    path('eliminarCarrito/', vi.remove_from_cart),

]
