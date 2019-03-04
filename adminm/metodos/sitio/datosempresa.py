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
		{"tipo":"char","valor":dato.banco,"label":"Banco:", "name":"banco"},
		{"tipo":"char","valor":dato.tipo_tarjeta,"label":"Tipo de tarjeta:", "name":"tipo_tarjeta"},
		{"tipo":"char","valor":dato.link_encuesta,"label":"Link a encuesta de servicio:", "name":"link_encuesta"},
		{"tipo":"char","valor":dato.direccion,"label":"Dirección:", "name":"direccion"},
		{"tipo":"char","valor":dato.telefono,"label":"Telefono:", "name":"telefono"},
		{"tipo":"char","valor":dato.correo,"label":"Correo electronico:", "name":"correo"},
		{"tipo":"char","valor":dato.correopaypal,"label":"Correo electronico de la cuenta paypal:", "name":"correopaypal"},

		{"tipo":"char","valor":dato.facebook,"label":"Link de Facebook:", "name":"facebook"},
		{"tipo":"char","valor":dato.twiter,"label":"Link de Twitter:", "name":"twiter"},
		{"tipo":"char","valor":dato.instagram,"label":"Link de Instagram:", "name":"instagram"},
		{"tipo":"char","valor":dato.youtube,"label":"Link de Youtube:", "name":"youtube"},

		{"tipo":"imagen2","valor":dato.logo.url,"label":"Logo:", "name":"logo"},
		{"tipo":"char", "valor":dato.titulo, "label":"Titulo de texto para mostrar en la parte baja del sitio:", "name":"titulo"},
		{"tipo":"text", "valor":dato.giro_de_la_empresa,"label":"Texto para mostrar en la parte baja del sitio:", "name":"giro"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificardato(request):
	empresa = Empresa.objects.last()
	imagen = empresa.logo
	
	if "logo" in request.FILES:
		dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
				direccion=request.POST.get("direccion"),
				telefono=request.POST.get("telefono"),
				correo=request.POST.get("correo"),
				correopaypal=request.POST.get("correopaypal"),
				logo=request.FILES["logo"],
				titulo=request.POST.get("titulo"),
				giro_de_la_empresa=request.POST.get("giro"),
				numero_de_cuenta=request.POST.get("numero_de_cuenta"),
				banco=request.POST.get("banco"),
				tipo_tarjeta=request.POST.get("tipo_tarjeta"),
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
				correopaypal=request.POST.get("correopaypal"),
				logo=imagen,
				titulo=request.POST.get("titulo"),
				giro_de_la_empresa=request.POST.get("giro"),
				numero_de_cuenta=request.POST.get("numero_de_cuenta"),
				banco=request.POST.get("banco"),
				tipo_tarjeta=request.POST.get("tipo_tarjeta"),
				link_encuesta=request.POST.get("link_encuesta"),
				facebook=request.POST.get("facebook"),
				twiter=request.POST.get("twiter"),
				instagram=request.POST.get("instagram"),
				youtube=request.POST.get("youtube"),)
	empresa.delete()
	return JsonResponse("Correcto", safe=False)