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

# Categorias
@csrf_exempt
def showcategorias(request):
	categorias = Categoria.objects.all()
	categorias = serializers.serialize('json', categorias)
	data = categorias
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarcategorias(request):
	categoria = Categoria.objects.get(id=request.POST.get("id"))
	data = {"nombre":{"tipo":"char","valor":categoria.nombre,"label":"Nombre:", "name":"nombre"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarcategorias(request):
	data = {"nombre":{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarcategoria(request):
	categoria = Categoria.objects.create(nombre=request.POST.get("nombre"),)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarcategoria(request):
	categoria = Categoria.objects.get(id=request.POST.get("idcategoria"))
	categoria.nombre=request.POST.get("nombre")
	categoria.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarcategoria(request):
	categoria = Categoria.objects.get(id=request.POST.get("id"))
	categoria.delete()
	return JsonResponse(id, safe=False)