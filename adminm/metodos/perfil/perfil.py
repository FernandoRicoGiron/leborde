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
def showmodificarperfil(request):
	perfil = request.user
	data = {"usuario":{"tipo":"char","valor":perfil.get_username(),"label":"Nombre de usuario:", "name":"usuario"},
		"nombre":{"tipo":"char","valor":perfil.first_name,"label":"Nombre:", "name":"nombre"},
		"apellido":{"tipo":"char","valor":perfil.last_name,"label":"Apellido:", "name":"apellido"},
		"email":{"tipo":"char","valor":perfil.email,"label":"Email:", "name":"email"},
		
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificarperfil(request):
	user = request.user
	user.username = request.POST.get("usuario")
	user.first_name = request.POST.get("nombre")
	user.last_name = request.POST.get("apellido")
	user.email = request.POST.get("email")
	user.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def cerrarsesion(request):
	logout(request)
	return redirect("/")