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

# FAQs
@csrf_exempt
def showpreguntas(request):
	preguntas = FAQ.objects.all()
	preguntas = serializers.serialize('json', preguntas)
	data = preguntas
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarpreguntas(request):
	pregunta = FAQ.objects.get(id=request.POST.get("id"))
	data = {"pregunta":{"tipo":"char","valor":pregunta.pregunta,"label":"Pregunta:", "name":"pregunta"},
		"respuesta":{"tipo":"ckeditor","valor":pregunta.respuesta,"label":"Respuesta:", "name":"respuesta"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarpreguntas(request):
	data = {"pregunta":{"tipo":"char","valor":"","label":"Pregunta:", "name":"pregunta"},
		"respuesta":{"tipo":"ckeditor","valor":"","label":"Respuesta:", "name":"respuesta"},
		}
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarpregunta(request):
	pregunta = FAQ.objects.create(pregunta=request.POST.get("pregunta"),
		respuesta=request.POST.get("respuesta"),)
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarpregunta(request):
	pregunta = FAQ.objects.get(id=request.POST.get("idpregunta"))
	pregunta.pregunta = request.POST.get("pregunta")
	pregunta.respuesta = request.POST.get("respuesta")
	pregunta.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarpregunta(request):
	pregunta = FAQ.objects.get(id=request.POST.get("id"))
	id=pregunta.id
	pregunta.delete()
	return JsonResponse(id, safe=False)