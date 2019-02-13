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

# QuienesSomoss
@csrf_exempt
def showquienessomos(request):
	quienessomos = QuienesSomos.objects.all()
	quienessomos = serializers.serialize('json', quienessomos)
	data = quienessomos
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarquienessomos(request):
	quisomos = QuienesSomos.objects.get(id=request.POST.get("id"))
	data = [{"tipo":"char","valor":quisomos.titulo,"label":"Titulo:", "name":"titulo"},
		{"tipo":"ckeditor","valor":quisomos.texto,"label":"Contenido:", "name":"texto"},
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarquienessomos(request):
	data = [{"tipo":"char","valor":"","label":"Titulo:", "name":"titulo"},
		{"tipo":"ckeditor","valor":"","label":"Contenido:", "name":"texto"},
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarquisomos(request):
	quisomos = QuienesSomos.objects.create(titulo=request.POST.get("titulo"),
		texto=request.POST.get("texto"),)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarquisomos(request):
	quisomos = QuienesSomos.objects.get(id=request.POST.get("idquisomos"))
	quisomos.titulo = request.POST.get("titulo")
	quisomos.texto = request.POST.get("texto")
	quisomos.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarquisomos(request):
	quisomos = QuienesSomos.objects.get(id=request.POST.get("id"))
	id=quisomos.id
	quisomos.delete()
	return JsonResponse(id, safe=False)