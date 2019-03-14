from django.shortcuts import render, redirect
from ecommerce.models import *
from administracion.models import *
from sitio.models import *
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from djmoney.money import Money
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from functools import reduce
from django.core import serializers
from django.contrib.auth.models import User
import sweetify
import operator
import json
# Productos
# Mostrar Productos
@csrf_exempt
def showproductos(request):
	productos = Producto.objects.all().order_by("id")
	imagenes = {}
	categorias = {}
	for producto in productos:
		if producto.imagenes:
			imagenes[producto.imagenes.first().id] = producto.imagenes.first().imagen.url
		categorias[producto.categoria.id] = producto.categoria.nombre
	productos = serializers.serialize('json', productos)
	data = {"productos":productos, "imagenes":imagenes, "categorias":categorias}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarproductos(request):
	producto = Producto.objects.get(id=request.POST.get("id"))
	imagenes = {}
	for imagen in producto.imagenes.all():
		imagenes[imagen.id] = {"id":imagen.id, "url":imagen.imagen.url}

	inventario_tallas = {}
	inv_tallas = Inventario_Talla.objects.filter(producto=producto)
	cont = 0
	for talla in inv_tallas:
		inventario_tallas[talla.id] = {"valor":talla.cantidad, "valor2":talla.talla.id,"label":"Inventario de " + talla.talla.nombre + " :", "name":"inventario"+str(talla.id),}

	data = [{"tipo":"char","valor":producto.nombre,"label":"Nombre:", "name":"nombre"},
			{"tipo":"text","valor":producto.descripcion,"label":"Descripción:", "name":"descripcion"},
			{"tipo":"bolean","valor":producto.popular,"label":"¿Es un producto popular?", "name":"popular"},
			{"tipo":"bolean","valor":producto.en_tienda,"label":"¿Este producto estara visible en la tienda?", "name":"en_tienda"},
			{"tipo":"money","valor":producto.precio.amount,"label":"Precio al publico:", "name":"precio"},
			{"tipo":"money","valor":producto.precio_oferta.amount,"label":"Precio sin oferta:", "name":"precio_oferta"},
			{"tipo":"select","valor":producto.categoria.nombre, "sel":producto.categoria.id, "label":"Categoria:", "opciones":serializers.serialize('json', Categoria.objects.all()), "name":"categoria"},
			{"tipo":"multiselect","valor":"","label":"Tallas:", "sel":serializers.serialize('json', producto.tallas.all()), "opciones":serializers.serialize('json', Talla.objects.all()), "name":"tallas"},
			{"tipo":"intdinamic","valor":inventario_tallas,},
			{"tipo":"imagen","valor":imagenes,"label":"Imagenes del producto: ", "name":"imagenes"},
			]
		
	# print(data)

	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarproductos(request):
	data = [{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
			{"tipo":"text","valor":"","label":"Descripción:", "name":"descripcion"},
			{"tipo":"bolean","valor":"","label":"¿Es un producto popular?", "name":"popular"},
			{"tipo":"bolean","valor":"","label":"¿Este producto estara visible en la tienda?", "name":"en_tienda"},
			{"tipo":"money","valor":"","label":"Precio al publico:", "name":"precio"},
			{"tipo":"money","valor":"","label":"Precio sin oferta:", "name":"precio_oferta"},
			# {"tipo":"int","valor":"","label":"Inventario:", "name":"inventario"},
			{"tipo":"select","valor":"","label":"Categoria:", "sel":"", "opciones":serializers.serialize('json', Categoria.objects.all()), "name":"categoria"},
			{"tipo":"multiselect","valor":"","label":"Tallas:", "sel":"", "opciones":serializers.serialize('json', Talla.objects.all()), "name":"tallas"},
			{"tipo":"imagen","valor":"","label":"Imagenes:","name":"imagenes"},
			]
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarproducto(request):
	print(request.POST)
	idimagenes = request.POST.getlist("idimagenes")
	listatallas = request.POST.getlist("tallas")
	tallas = Talla.objects.filter(id__in=listatallas)
	if len(idimagenes) > 0:
		if request.POST.get("popular"):
			popular=True
		else:
			popular=False
		if request.POST.get("en_tienda"):
			en_tienda=True
		else:
			en_tienda=False
		sumainventario = 0
		for x in request.POST.getlist("tallas"):
			
			valor = request.POST.get("inventario"+str(x))
			sumainventario += int(valor)
		categoria = Categoria.objects.get(id=request.POST.get("categoria"))
		producto = Producto.objects.create(nombre=request.POST.get("nombre"),
			descripcion=request.POST.get("descripcion"),
			precio=request.POST.get("precio"),
			precio_oferta=request.POST.get("precio_oferta"),
			popular=popular,
			en_tienda=en_tienda,
			inventario=sumainventario,
			categoria=categoria)
		producto.tallas.add(*tallas)
		for imagenid in idimagenes:
			imagen = Imagen.objects.get(id=imagenid)
			producto.imagenes.add(imagen)

		for x in request.POST.getlist("tallas"):
			inventario = request.POST["inventario"+str(x)]
			talla = request.POST["talla"+str(x)]
			talla = Talla.objects.get(id=talla)
			Inventario_Talla.objects.create(producto=producto, talla=talla, cantidad=inventario)
		return JsonResponse("Correcto", safe=False)
	else:
		return JsonResponse("Verifique que ingreso todos los datos por favor", safe=False)

@csrf_exempt
def modificarproducto(request):
	print(request.POST)
	producto = Producto.objects.get(id=request.POST.get("idproducto"))
	idimagenes = request.POST.getlist("idimagenes")
	idimagenesnu = request.POST.getlist("idimagenesnu")
	listatallas = request.POST.getlist("tallas")
	tallas = Talla.objects.filter(id__in=listatallas)
	if len(idimagenes) > 0 or len(idimagenesnu) > 0:
		if request.POST.get("popular"):
			popular=True
		else:
			popular=False
		if request.POST.get("en_tienda"):
			en_tienda=True
		else:
			en_tienda=False
		categoria = Categoria.objects.get(id=request.POST.get("categoria"))
		sumainventario = 0
		for x in request.POST.getlist("tallas"):
			valor = request.POST.get("inventario"+str(x))
			sumainventario += int(valor)
		producto.tallas.clear()
		producto.nombre=request.POST.get("nombre")
		producto.descripcion=request.POST.get("descripcion")
		producto.precio=request.POST.get("precio")
		producto.precio_oferta=request.POST.get("precio_oferta")
		producto.popular=popular
		producto.en_tienda=en_tienda
		producto.inventario=sumainventario
		producto.categoria=categoria
		producto.tallas.add(*tallas)

		for imagenproducto in producto.imagenes.all():
			if len(idimagenes) == 0:
				imagenproducto.delete()
			elif str(imagenproducto.id) not in idimagenes:
				imagenproducto.delete()

		for imagenid in idimagenesnu:
			imagen = Imagen.objects.get(id=imagenid)
			producto.imagenes.add(imagen)
		producto.save()

		Inventario_Talla.objects.filter(producto=producto).delete()
		for x in request.POST.getlist("tallas"):
			inventario = request.POST["inventario"+str(x)]
			talla = request.POST["talla"+str(x)]
			talla = Talla.objects.get(id=talla)
			Inventario_Talla.objects.create(producto=producto, talla=talla, cantidad=inventario)
		return JsonResponse("Correcto", safe=False)
	else:
		return JsonResponse("Verifique que ingreso todos los datos por favor", safe=False)

@csrf_exempt
def eliminarproducto(request):
	producto = Producto.objects.get(id=request.POST.get("id"))
	id = producto.id
	for imagen in producto.imagenes.all():
		imagen.delete()
	producto.delete()
	return JsonResponse(id, safe=False)