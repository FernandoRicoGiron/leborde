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
    path('faqs/', vi.faqs),
    # Autentificacion
    path('modificardatos/', vi.modificardatos),
    path('modificarcontraseña/', vi.modificarcontraseña),
    path('req_sesion/', vi.req_sesion),
    path('registrar/', vi.registrar),
    path('login/', vi.iniciarsesion),
    path('logout/', vi.cerrarsesion),
    path('recuperarcontraseña/', vi.recuperarcontraseña),
    path('cambiarpassword/', vi.cambiarpassword),
	path('modificarcontraseña/', vi.modificarcontra),
    path('perfil/', vi.perfil),
    # Ecommerce
    path('agregarCarrito/', vi.add_to_cart),
    path('eliminarCarrito/', vi.remove_from_cart),
    path('pagar/', vi.pago),
    # PAYPAL
    path('pagadopaypal/', vi.pagadopaypal, name="pagadopaypal"),
    path('errorpagadopaypal/', vi.errorpagadopaypal, name="errorpagadopaypal"),
    path("pagar/paypal/", vi.pagarpaypal, name="paypalpag"),
    path("ipn/", vi.ipn, name="webhook")

]
