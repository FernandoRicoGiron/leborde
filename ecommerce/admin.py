from django.contrib import admin
from .models import *

class Productos(admin.ModelAdmin):
	list_display = ["id","nombre"]
	list_display_links = ["id","nombre"]
	search_fields = ['nombre']
	filter_horizontal = ['imagenes']
	 
	class Meta:
		model = Producto

# Tienda
admin.site.register(Imagen)
admin.site.register(Categoria)
admin.site.register(Talla)
admin.site.register(Producto, Productos)
admin.site.register(Ficha_Tecnica)
admin.site.register(Coleccion)
admin.site.register(Envio)
admin.site.register(Num_Pedido)
admin.site.register(Inventario_Talla)
