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

# Tallas
@csrf_exempt
def showtallas(request):
	tallas = Talla.objects.all()
	tallas = serializers.serialize('json', tallas)
	data = tallas
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificartallas(request):
	talla = Talla.objects.get(id=request.POST.get("id"))
	data = [{"tipo":"char","valor":talla.nombre,"label":"Nombre:", "name":"nombre"},
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregartallas(request):
	data = [{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregartalla(request):
	talla = Talla.objects.create(nombre=request.POST.get("nombre"),)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificartalla(request):
	talla = Talla.objects.get(id=request.POST.get("idtalla"))
	talla.nombre=request.POST.get("nombre")
	talla.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminartalla(request):
	talla = Talla.objects.get(id=request.POST.get("id"))
	talla.delete()
	return JsonResponse(id, safe=False)