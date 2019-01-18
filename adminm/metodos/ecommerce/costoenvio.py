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
def showmodificarenvio(request):
	dato = Envio.objects.last()
	data = [{"tipo":"money","valor":dato.costo.amount,"label":"Costo de Envios:", "name":"costo"},
		
		]
	return JsonResponse(data, safe=False)

@csrf_exempt
def modificarenvio(request):
	dato = Envio.objects.last()
	dato.delete()
	dato = Envio.objects.create(costo=request.POST.get("costo"),)
	return JsonResponse("Correcto", safe=False)