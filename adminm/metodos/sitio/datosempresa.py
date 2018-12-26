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
from django.contrib.auth.hashers import check_password
import sweetify
import operator
import json


@csrf_exempt
def showmodificardatos(request):
	dato = Empresa.objects.last()
	data = {"nombre":{"tipo":"char","valor":dato.nombre,"label":"Nombre:", "name":"nombre"},
		"logo":{"tipo":"imagen2","valor":dato.logo.url,"label":"Logo:", "name":"logo"},
		"mision":{"tipo":"ckeditor","valor":dato.mision,"label":"Misión:", "name":"mision"},
		"vision":{"tipo":"ckeditor","valor":dato.vision,"label":"Visión:", "name":"vision"},
		"valores":{"tipo":"ckeditor","valor":dato.valores,"label":"Valores:", "name":"valores"},
		"historia":{"tipo":"ckeditor","valor":dato.historia,"label":"Historia:", "name":"historia"},
		"giro":{"tipo":"ckeditor","valor":dato.giro_de_la_empresa,"label":"Giro de la empresa:", "name":"giro"},
		
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificardato(request):
	dato = Empresa.objects.last()
	imagen = dato.logo
	dato.delete()
	if "logo" in request.FILES:
		dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
				logo=request.FILES["logo"],
				mision=request.POST.get("mision"),
				vision=request.POST.get("vision"),
				valores=request.POST.get("valores"),
				historia=request.POST.get("historia"),
				giro_de_la_empresa=request.POST.get("giro"))
	else:
		dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
				logo=imagen,
				mision=request.POST.get("mision"),
				vision=request.POST.get("vision"),
				valores=request.POST.get("valores"),
				historia=request.POST.get("historia"),
				giro_de_la_empresa=request.POST.get("giro"))
	return JsonResponse("Correcto", safe=False)