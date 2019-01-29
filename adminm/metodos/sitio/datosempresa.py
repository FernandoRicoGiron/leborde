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
	data = [{"tipo":"char","valor":dato.nombre,"label":"Nombre:", "name":"nombre"},
		{"tipo":"char","valor":dato.numero_de_cuenta,"label":"Número de cuenta:", "name":"numero_de_cuenta"},
		{"tipo":"char","valor":dato.link_encuesta,"label":"Link a encuesta de servicio:", "name":"link_encuesta"},
		{"tipo":"char","valor":dato.direccion,"label":"Dirección:", "name":"direccion"},
		{"tipo":"char","valor":dato.telefono,"label":"Telefono:", "name":"telefono"},
		{"tipo":"char","valor":dato.correo,"label":"Correo electronico:", "name":"correo"},

		{"tipo":"char","valor":dato.facebook,"label":"Link de Facebook:", "name":"facebook"},
		{"tipo":"char","valor":dato.twiter,"label":"Link de Twitter:", "name":"twiter"},
		{"tipo":"char","valor":dato.instagram,"label":"Link de Instagram:", "name":"instagram"},
		{"tipo":"char","valor":dato.youtube,"label":"Link de Youtube:", "name":"youtube"},

		{"tipo":"imagen2","valor":dato.logo.url,"label":"Logo:", "name":"logo"},
		{"tipo":"ckeditor","valor":dato.mision,"label":"Misión:", "name":"mision"},
		{"tipo":"ckeditor","valor":dato.vision,"label":"Visión:", "name":"vision"},
		{"tipo":"ckeditor","valor":dato.valores,"label":"Valores:", "name":"valores"},
		{"tipo":"ckeditor","valor":dato.que_es,"label":"¿Que es "+dato.nombre+"?:", "name":"que_es"},
		{"tipo":"ckeditor","valor":dato.historia,"label":"Historia:", "name":"historia"},
		{"tipo":"ckeditor","valor":dato.giro_de_la_empresa,"label":"Giro de la empresa:", "name":"giro"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificardato(request):
	dato = Empresa.objects.last()
	imagen = dato.logo
	dato.delete()
	if "logo" in request.FILES:
		dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
				direccion=request.POST.get("direccion"),
				telefono=request.POST.get("telefono"),
				correo=request.POST.get("correo"),
				logo=request.FILES["logo"],
				mision=request.POST.get("mision"),
				vision=request.POST.get("vision"),
				valores=request.POST.get("valores"),
				historia=request.POST.get("historia"),
				que_es=request.POST.get("que_es"),
				giro_de_la_empresa=request.POST.get("giro"),
				numero_de_cuenta=request.POST.get("numero_de_cuenta"),
				link_encuesta=request.POST.get("link_encuesta"),
				facebook=request.POST.get("facebook"),
				twiter=request.POST.get("twiter"),
				instagram=request.POST.get("instagram"),
				youtube=request.POST.get("youtube"),)
	else:
		dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
				direccion=request.POST.get("direccion"),
				telefono=request.POST.get("telefono"),
				correo=request.POST.get("correo"),
				logo=imagen,
				mision=request.POST.get("mision"),
				vision=request.POST.get("vision"),
				valores=request.POST.get("valores"),
				historia=request.POST.get("historia"),
				que_es=request.POST.get("que_es"),
				giro_de_la_empresa=request.POST.get("giro"),
				numero_de_cuenta=request.POST.get("numero_de_cuenta"),
				link_encuesta=request.POST.get("link_encuesta"),
				facebook=request.POST.get("facebook"),
				twiter=request.POST.get("twiter"),
				instagram=request.POST.get("instagram"),
				youtube=request.POST.get("youtube"),)
	return JsonResponse("Correcto", safe=False)