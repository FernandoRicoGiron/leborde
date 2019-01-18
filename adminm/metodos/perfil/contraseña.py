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
def showmodificarcontraseña(request):
	contraseña = Empresa.objects.last()
	data = [{"tipo":"label","label":" Modificar Contraseña"},
		{"tipo":"pass","valor":"","label":"Nueva Contraseña:", "name":"contraseña"},
		{"tipo":"pass","valor":"","label":"Repetir Contraseña:", "name":"recontraseña"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificarcontraseña(request):
	usuario = request.user.username
	if request.POST.get("contraseña") == request.POST.get("recontraseña"):
		request.user.set_password(request.POST.get("contraseña"))
		request.user.save()
		user = authenticate(request, username=usuario, password=request.POST.get("contraseña"))
		login(request, user)
		return JsonResponse("Correcto", safe=False)
	else:
		return JsonResponse("Incorrecto", safe=False)
	return JsonResponse("Correcto", safe=False)