from django.contrib import admin
from .models import *

# Tienda
admin.site.register(Imagen)
admin.site.register(Categoria)
admin.site.register(Talla)
admin.site.register(Producto)
admin.site.register(Ficha_Tecnica)
admin.site.register(Coleccion)
admin.site.register(Envio)
admin.site.register(Num_Pedido)
