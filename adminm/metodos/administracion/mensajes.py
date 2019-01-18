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
from django.core.mail import EmailMessage, send_mail
import sweetify
import operator
import json
# Mensajes
@csrf_exempt
def showmensajes(request):
	mensajes = Mensaje.objects.all()
	mensajes = serializers.serialize('json', mensajes)
	data = {"mensajes":mensajes}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarmensajes(request):
	mensaje = Mensaje.objects.get(id=request.POST.get("id"))
	data = [{"tipo":"char","valor":mensaje.nombre,"label":"Nombre:", "name":"nombre"},
			{"tipo":"char","valor":mensaje.asunto, "label":"Asusnto:", "name":"asunto"},
			{"tipo":"char","valor":mensaje.email,"label":"Correo Electrónico:", "name":"email"},
			{"tipo":"text","valor":mensaje.mensaje,"label":"Mensaje:", "name":"mensajeusu"},
			{"tipo":"text2","valor":"","label":"Contestar:", "name":"mensaje"},
			]
	mensaje.estado = "Leido"
	mensaje.save()
	return JsonResponse(data, safe=False)

@csrf_exempt
def contestarmensaje(request):
	print(request.POST)
	mensaje = Mensaje.objects.get(id = request.POST.get("idmensaje"))
	if request.POST.get("mensaje") != "":
		send_mail(
			'Contestacion a ' + mensaje.asunto,
			request.POST.get("mensaje"),
			'unipymes.tec@gmail.com',
			[mensaje.email],
			fail_silently=False,
		)
		return JsonResponse("Correcto", safe=False)
	else:
		return JsonResponse("Incorrecto", safe=False)

@csrf_exempt
def eliminarmensaje(request):
	mensaje = Mensaje.objects.get(id=request.POST.get("id"))
	id = mensaje.id
	mensaje.delete()
	return JsonResponse(id, safe=False)