from django.contrib import admin
from .models import *
# Pedido
admin.site.register(Pedido)
admin.site.register(Producto_Pedido)
admin.site.register(Cliente)
admin.site.register(Mensaje)
admin.site.register(Venta)