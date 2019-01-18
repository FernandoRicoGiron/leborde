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
# Colecciones
@csrf_exempt
def showcolecciones(request):
	colecciones = Coleccion.objects.all()
	colecciones = serializers.serialize('json', colecciones)
	data = colecciones
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarcolecciones(request):
	coleccion = Coleccion.objects.get(id=request.POST.get("id"))
	print(request.POST.get("id"))
	data = [{"tipo":"char","valor":coleccion.nombre,"label":"Nombre:", "name":"nombre"},
			{"tipo":"imagen2","valor":coleccion.imagen_representativa.url,"label":"Imagen:", "name":"imagen"},
			{"tipo":"multiselect","valor":"","label":"Productos:", "sel":serializers.serialize('json', coleccion.productos.all()), "opciones":serializers.serialize('json', Producto.objects.all()), "name":"productos"},
			]
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarcolecciones(request):
	data = [{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
			{"tipo":"imagen2","valor":"","label":"Imagen:", "name":"imagen"},
			{"tipo":"multiselect","valor":"","label":"Productos:", "sel":"", "opciones":serializers.serialize('json', Producto.objects.all()), "name":"productos"},
			]
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarcoleccion(request):
	listaproductos = request.POST.getlist("productos")
	productos = Producto.objects.filter(id__in=listaproductos)
	coleccion = Coleccion.objects.create(nombre=request.POST.get("nombre"),
		imagen_representativa=request.FILES["imagen"])
	coleccion.productos.add(*productos)
	coleccion.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarcoleccion(request):
	print(request.POST)
	listaproductos = request.POST.getlist("productos")
	productos = Producto.objects.filter(id__in=listaproductos)
	coleccion = Coleccion.objects.get(id=request.POST.get("idcoleccion"))
	coleccion.productos.clear()
	coleccion.nombre=request.POST.get("nombre")
	if "imagen" in request.FILES:
		coleccion.imagen_representativa = request.FILES["imagen"]
	coleccion.productos.add(*productos)
	coleccion.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarcoleccion(request):
	coleccion = Coleccion.objects.get(id=request.POST.get("id"))
	id = coleccion.id
	coleccion.delete()
	return JsonResponse(id, safe=False)