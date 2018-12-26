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

# Carrusels
@csrf_exempt
def showcarruseles(request):
	carruseles = Carrusel.objects.all()
	carruseles = serializers.serialize('json', carruseles)
	data = carruseles
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarcarruseles(request):
	carrusel = Carrusel.objects.get(id=request.POST.get("id"))
	data = {"texto":{"tipo":"char","valor":carrusel.texto,"label":"Texto:", "name":"texto"},
		"url":{"tipo":"char","valor":carrusel.url,"label":"Url:", "name":"url"},
		"imagen":{"tipo":"imagen2","valor":carrusel.imagen.url,"label":"Imagen:", "name":"imagen"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarcarruseles(request):
	data = {"texto":{"tipo":"char","valor":"","label":"Texto:", "name":"texto"},
		"url":{"tipo":"char","valor":"","label":"Url:", "name":"url"},
		"imagen":{"tipo":"imagen2","valor":"","label":"Imagen:", "name":"imagen"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarcarrusel(request):
	carrusel = Carrusel.objects.create(texto=request.POST.get("texto"),
		url=request.POST.get("url"),
		imagen=request.FILES["imagen"],)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarcarrusel(request):
	carrusel = Carrusel.objects.get(id=request.POST.get("idcarrusel"))
	carrusel.texto = request.POST.get("texto")
	carrusel.url = request.POST.get("url")
	if "imagen" in request.FILES:
		carrusel.imagen = request.FILES["imagen"]
	carrusel.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarcarrusel(request):
	carrusel = Carrusel.objects.get(id=request.POST.get("id"))
	id=carrusel.id
	carrusel.delete()
	return JsonResponse(id, safe=False)