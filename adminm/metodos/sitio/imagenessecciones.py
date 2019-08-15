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
def showmodificarsecciones(request):
	seccion = Secciones.objects.last()
	data = [{"tipo":"char","valor":seccion.titulot,"label":"Titulo en 'Tienda':", "name":"titulot"},
		{"tipo":"imagen2","valor":seccion.imagent.url,"label":"Imagen principal en 'Tienda':", "name":"imagent"},
		{"tipo":"char","valor":seccion.tituloqs,"label":"Titulo en '¿Quiénes Somos?':", "name":"tituloqs"},
		{"tipo":"imagen2","valor":seccion.imagenqs.url,"label":"Imagen principal en '¿Quiénes Somos?':", "name":"imagenqs"},
		{"tipo":"char","valor":seccion.tituloc,"label":"Titulo en 'Contáctanos':", "name":"tituloc"},
		{"tipo":"imagen2","valor":seccion.imagenc.url,"label":"Imagen principal en 'Contáctanos':", "name":"imagenc"},
		{"tipo":"char","valor":seccion.titulodp,"label":"Titulo en 'Datos para pago':", "name":"titulodp"},
		{"tipo":"imagen2","valor":seccion.imagendp.url,"label":"Imagen principal en 'Datos para pago':", "name":"imagendp"},

		{"tipo":"char","valor":seccion.tituloppaypal,"label":"Titulo en 'Proceder al pago con paypal':", "name":"tituloppaypal"},
		{"tipo":"imagen2","valor":seccion.imagenppaypal.url,"label":"Imagen principal en 'Proceder al pago con paypal':", "name":"imagenppaypal"},

		{"tipo":"char","valor":seccion.titulop,"label":"Titulo en 'Datos de Perfil':", "name":"titulop"},
		{"tipo":"imagen2","valor":seccion.imagenp.url,"label":"Imagen principal en 'Datos de Perfil':", "name":"imagenp"},
		{"tipo":"char","valor":seccion.titulopedidos,"label":"Titulo en 'Pedidos':", "name":"titulopedidos"},
		{"tipo":"imagen2","valor":seccion.imagenpedidos.url,"label":"Imagen principal en 'Pedidos':", "name":"imagenpedidos"},
		{"tipo":"char","valor":seccion.titulopreguntas,"label":"Titulo en 'Preguntas Frecuentes':", "name":"titulopreguntas"},
		{"tipo":"imagen2","valor":seccion.imagenpreguntas.url,"label":"Imagen principal en 'Preguntas Frecuentes':", "name":"imagenpreguntas"},

		{"tipo":"char","valor":seccion.tituloterminos,"label":"Titulo en 'Terminos y condiciones':", "name":"tituloterminos"},
		{"tipo":"imagen2","valor":seccion.imagenterminos.url,"label":"Imagen principal en 'Terminos y condiciones':", "name":"imagenterminos"},

		{"tipo":"char","valor":seccion.titulopoliticas,"label":"Titulo en 'Aviso de privacidad':", "name":"titulopoliticas"},
		{"tipo":"imagen2","valor":seccion.imagenpoliticas.url,"label":"Imagen principal en 'Aviso de privacidad':", "name":"imagepoliticass"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificarseccion(request):
	print(request.POST)
	print(request.FILES)
	seccion = Secciones.objects.last()
	imagent = seccion.imagent
	imagenqs = seccion.imagenqs
	imagenc = seccion.imagenc
	imagendp = seccion.imagendp
	imagenppaypal = seccion.imagenppaypal
	imagenp = seccion.imagenp
	imagenpedidos = seccion.imagenpedidos
	imagenpreguntas = seccion.imagenpreguntas
	imagenpoliticas = seccion.imagenpoliticas
	imagenterminos = seccion.imagenterminos

	if "imagent" in request.FILES:
		imagent = request.FILES["imagent"]
	if "imagenqs" in request.FILES:
		imagenqs = request.FILES["imagenqs"]
	if "imagenc" in request.FILES:
		imagenc = request.FILES["imagenc"]
	if "imagendp" in request.FILES:
		imagendp = request.FILES["imagendp"]

	if "imagenppaypal" in request.FILES:
		imagenppaypal = request.FILES["imagenppaypal"]

	if "imagenp" in request.FILES:
		imagenp = request.FILES["imagenp"]
	if "imagenpedidos" in request.FILES:
		imagenpedidos = request.FILES["imagenpedidos"]
	if "imagenpreguntas" in request.FILES:
		imagenpreguntas = request.FILES["imagenpreguntas"]

	if "imagenterminos" in request.FILES:
		imagenterminos = request.FILES["imagenterminos"]
	if "imagepoliticass" in request.FILES:
		imagenpoliticas = request.FILES["imagepoliticass"]

	seccion.delete()

	seccion = Secciones.objects.create(titulot=request.POST.get("titulot"),
			imagent=imagent,
			tituloqs=request.POST.get("tituloqs"),
			imagenqs=imagenqs,
			tituloc=request.POST.get("tituloc"),
			imagenc=imagenc,
			titulodp=request.POST.get("titulodp"),
			imagendp=imagendp,

			tituloppaypal=request.POST.get("tituloppaypal"),
			imagenppaypal=imagenppaypal,

			titulop=request.POST.get("titulop"),
			imagenp=imagenp,
			titulopedidos=request.POST.get("titulopedidos"),
			imagenpedidos=imagenpedidos,
			titulopreguntas=request.POST.get("titulopreguntas"),
			imagenpreguntas=imagenpreguntas,
			tituloterminos=request.POST.get("tituloterminos"),
			imagenterminos=imagenterminos,
			titulopoliticas=request.POST.get("titulopoliticas"),
			imagenpoliticas=imagenpoliticas,
			)

	return JsonResponse("Correcto", safe=False)