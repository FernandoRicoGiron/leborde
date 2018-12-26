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

# Marcas
@csrf_exempt
def showmarcas(request):
	marcas = Marca.objects.all()
	marcas = serializers.serialize('json', marcas)
	data = marcas
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarmarcas(request):
	marca = Marca.objects.get(id=request.POST.get("id"))
	data = {"nombre":{"tipo":"char","valor":marca.nombre,"label":"Texto:", "name":"nombre"},
		"imagen":{"tipo":"imagen2","valor":marca.imagen.url,"label":"Imagen:", "name":"imagen"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarmarcas(request):
	data = {"nombre":{"tipo":"char","valor":"","label":"Texto:", "name":"nombre"},
		"imagen":{"tipo":"imagen2","valor":"","label":"Imagen:", "name":"imagen"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarmarca(request):
	marca = Marca.objects.create(nombre=request.POST.get("nombre"),
		imagen=request.FILES["imagen"],)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarmarca(request):
	marca = Marca.objects.get(id=request.POST.get("idmarca"))
	marca.nombre = request.POST.get("nombre")
	if "imagen" in request.FILES:
		marca.imagen = request.FILES["imagen"]
	marca.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarmarca(request):
	marca = Marca.objects.get(id=request.POST.get("id"))
	id=marca.id
	marca.delete()
	return JsonResponse(id, safe=False)