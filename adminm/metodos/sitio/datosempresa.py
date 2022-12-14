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
	logo = ""
	fav_logo = ""
	if dato.logo:
		logo = dato.logo.url
	if dato.fav_logo:
		fav_logo = dato.fav_logo.url
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

		{"tipo":"imagen2","valor":logo,"label":"Logo:", "name":"logo"},
		{"tipo":"imagen2","valor":fav_logo,"label":"Logo de pestaña:", "name":"logo2"},
		{"tipo":"char", "valor":dato.titulo, "label":"Titulo de texto para mostrar en la parte baja del sitio:", "name":"titulo"},
		{"tipo":"text", "valor":dato.giro_de_la_empresa,"label":"Texto para mostrar en la parte baja del sitio:", "name":"giro"},
		{"tipo":"ckeditor", "valor":dato.terminos_condiciones,"label":"Terminos y Condiciones:", "name":"terminos_condiciones"},
		{"tipo":"ckeditor", "valor":dato.politicas,"label":"Politicas de Privacidad:", "name":"politicas"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificardato(request):
	empresa = Empresa.objects.last()
	imagen = empresa.logo
	imagen2 = empresa.fav_logo
	
	dato = Empresa.objects.create(nombre=request.POST.get("nombre"),
			direccion=request.POST.get("direccion"),
			telefono=request.POST.get("telefono"),
			correo=request.POST.get("correo"),
			logo=imagen,
			fav_logo=imagen2,
			correopaypal=request.POST.get("correopaypal"),
			titulo=request.POST.get("titulo"),
			giro_de_la_empresa=request.POST.get("giro"),
			numero_de_cuenta=request.POST.get("numero_de_cuenta"),
			banco=request.POST.get("banco"),
			tipo_tarjeta=request.POST.get("tipo_tarjeta"),
			link_encuesta=request.POST.get("link_encuesta"),
			facebook=request.POST.get("facebook"),
			twiter=request.POST.get("twiter"),
			instagram=request.POST.get("instagram"),
			youtube=request.POST.get("youtube"),
			terminos_condiciones=request.POST.get("terminos_condiciones"),
			politicas=request.POST.get("politicas"),
			
			)
	if "logo" in request.FILES:
		dato.logo=request.FILES["logo"]
	if "logo2" in request.FILES:
		dato.fav_logo=request.FILES["logo2"]
	dato.save()
	empresa.delete()
	return JsonResponse("Correcto", safe=False)