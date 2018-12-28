from django.urls import path, re_path
from django.conf.urls import include
from . import views as vi

urlpatterns = [
    path('', vi.index),
    path('nosotros/', vi.nosotros),
    re_path('tienda/(?P<id>\d+)/', vi.producto),
    path('tienda/', vi.tienda),
    path('contacto/', vi.contacto),

]
