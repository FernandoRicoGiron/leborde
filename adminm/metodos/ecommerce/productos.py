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
	productos = Producto.objects.all()
	imagenes = {}
	categorias = {}
	for producto in productos:
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
	data = {"nombre":{"tipo":"char","valor":producto.nombre,"label":"Nombre:", "name":"nombre"},
		"descripcion":{"tipo":"text","valor":producto.descripcion,"label":"Descripción:", "name":"descripcion"},
		"popular":{"tipo":"bolean","valor":producto.popular,"label":"¿Es un producto popular?", "name":"popular"},
		"precio":{"tipo":"money","valor":producto.precio.amount,"label":"Precio:", "name":"precio"},
		"precio_oferta":{"tipo":"money","valor":producto.precio_oferta.amount,"label":"Precio Oferta:", "name":"precio_oferta"},
		"inventario":{"tipo":"int","valor":producto.inventario,"label":"Inventario:", "name":"inventario"},
		"categorias":{"tipo":"select","valor":producto.categoria.nombre, "sel":producto.categoria.id, "label":"Categoria:", "opciones":serializers.serialize('json', Categoria.objects.all()), "name":"categoria"},
		"tallas":{"tipo":"multiselect","valor":"","label":"Tallas:", "sel":serializers.serialize('json', producto.tallas.all()), "opciones":serializers.serialize('json', Talla.objects.all()), "name":"tallas"},
		"imagenes":{"tipo":"imagen","valor":imagenes,"label":"Imagenes del producto: ", "name":"imagenes"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarproductos(request):
	data = {"nombre":{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
		"descripcion":{"tipo":"text","valor":"","label":"Descripción:", "name":"descripcion"},
		"popular":{"tipo":"bolean","valor":"","label":"¿Es un producto popular?", "name":"popular"},
		"precio":{"tipo":"money","valor":"","label":"Precio:", "name":"precio"},
		"precio_oferta":{"tipo":"money","valor":"","label":"Precio Oferta:", "name":"precio_oferta"},
		"inventario":{"tipo":"int","valor":"","label":"Inventario:", "name":"inventario"},
		"categorias":{"tipo":"select","valor":"","label":"Categoria:", "sel":"", "opciones":serializers.serialize('json', Categoria.objects.all()), "name":"categoria"},
		"tallas":{"tipo":"multiselect","valor":"","label":"Tallas:", "sel":"", "opciones":serializers.serialize('json', Talla.objects.all()), "name":"tallas"},
		"imagenes":{"tipo":"imagen","valor":"","label":"Imagenes:","name":"imagenes"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarproducto(request):
	idimagenes = request.POST.getlist("idimagenes")
	listatallas = request.POST.getlist("tallas")
	tallas = Talla.objects.filter(id__in=listatallas)
	if len(idimagenes) > 0:
		if request.POST.get("popular"):
			popular=True
		else:
			popular=False
		
		categoria = Categoria.objects.get(id=request.POST.get("categoria"))
		producto = Producto.objects.create(nombre=request.POST.get("nombre"),
			descripcion=request.POST.get("descripcion"),
			precio=request.POST.get("precio"),
			precio_oferta=request.POST.get("precio_oferta"),
			popular=popular,
			inventario=request.POST.get("inventario"),
			categoria=categoria)
		producto.tallas.add(*tallas)
		for imagenid in idimagenes:
			imagen = Imagen.objects.get(id=imagenid)
			producto.imagenes.add(imagen)
		return JsonResponse("Correcto", safe=False)
	else:
		return JsonResponse("Verifique que ingreso todos los datos por favor", safe=False)

@csrf_exempt
def modificarproducto(request):
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
		categoria = Categoria.objects.get(id=request.POST.get("categoria"))

		producto.tallas.clear()
		producto.nombre=request.POST.get("nombre")
		producto.descripcion=request.POST.get("descripcion")
		producto.precio=request.POST.get("precio")
		producto.precio_oferta=request.POST.get("precio_oferta")
		producto.popular=popular
		producto.inventario=request.POST.get("inventario")
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