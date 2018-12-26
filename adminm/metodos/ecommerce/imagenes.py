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
# Imagenes
@csrf_exempt
def agregarimagenes(request):
	data = {}
	for x in request.FILES.getlist("imagenes"):
		imagen = Imagen.objects.create(imagen=x)
		data[imagen.id] = {"url":imagen.imagen.url, "id":imagen.id}
	return JsonResponse(data, safe=False)

@csrf_exempt
def eliminarimagenes(request):
	print(request.POST.get("id"))
	imagen = Imagen.objects.get(id=request.POST.get("id"))
	id = imagen.id
	imagen.delete()
	return JsonResponse(id, safe=False)