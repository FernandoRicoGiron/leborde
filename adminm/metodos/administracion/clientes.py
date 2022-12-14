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
# Clientes
@csrf_exempt
def showclientes(request):
	clientes = Cliente.objects.all()
	usuarios = User.objects.all()
	clientes = serializers.serialize('json', clientes)
	listusuarios = {}
	for usuario in usuarios:
		listusuarios[usuario.id] = {"id":usuario.id,
			"username":usuario.username,
			"first_name":usuario.first_name,
			"last_name":usuario.last_name,
			"email":usuario.last_name}
	data = {"clientes":clientes, "usuarios":listusuarios}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarclientes(request):
	cliente = Cliente.objects.get(id=request.POST.get("id"))
	data = [{"tipo":"char","valor":cliente.usuario.first_name,"label":"Nombre:", "name":"nombre"},
			{"tipo":"char","valor":cliente.usuario.last_name,"label":"Apellido:", "name":"apellido"},
			{"tipo":"char","valor":cliente.usuario.email,"label":"Correo Electrónico:", "name":"email"},
			{"tipo":"char","valor":cliente.telefono,"label":"Telefono:", "name":"telefono"},
			{"tipo":"char","valor":cliente.colonia,"label":"Colonia:", "name":"colonia"},
			{"tipo":"char","valor":cliente.calle,"label":"Calle:", "name":"calle"},
			{"tipo":"char","valor":cliente.no_exterior,"label":"No. Exterior:", "name":"no_exterior"},
			{"tipo":"char","valor":cliente.no_interior,"label":"No. Interior:", "name":"no_interior"},
			{"tipo":"char","valor":cliente.ciudad,"label":"Ciudad:", "name":"ciudad"},
			{"tipo":"char","valor":cliente.estado,"label":"Estado:", "name":"estado"},
			{"tipo":"char","valor":cliente.pais,"label":"País:", "name":"pais"},
			{"tipo":"char","valor":cliente.codigopostal,"label":"Codigo Postal:", "name":"codigopostal"},
			{"tipo":"char","valor":cliente.usuario.username,"label":"Nombre de usuario:", "name":"usuario"},
			{"tipo":"label","label":" Modificar Contraseña (Solo llenar si desea modificar la contraseña)"},
			{"tipo":"pass","valor":"","label":"Nueva Contraseña:", "name":"contraseña"},
			{"tipo":"pass","valor":"","label":"Repetir Contraseña:", "name":"recontraseña"},]
		
		
	return JsonResponse(data, safe=False)

@csrf_exempt
def showagregarclientes(request):
	data = [{"tipo":"char","valor":"","label":"Nombre:", "name":"nombre"},
			{"tipo":"char","valor":"","label":"Apellido:", "name":"apellido"},
			{"tipo":"char","valor":"","label":"Correo Electrónico:", "name":"email"},
			{"tipo":"char","valor":"","label":"Telefono:", "name":"telefono"},
			{"tipo":"char","valor":"","label":"Colonia:", "name":"colonia"},
			{"tipo":"char","valor":"","label":"Calle:", "name":"calle"},
			{"tipo":"char","valor":"","label":"No. Exterior:", "name":"no_exterior"},
			{"tipo":"char","valor":"","label":"No. Interior:", "name":"no_interior"},
			{"tipo":"char","valor":"","label":"Ciudad:", "name":"ciudad"},
			{"tipo":"char","valor":"","label":"Estado:", "name":"estado"},
			{"tipo":"char","valor":"","label":"País:", "name":"pais"},
			{"tipo":"char","valor":"","label":"Codigo Postal:", "name":"codigopostal"},
			{"tipo":"char","valor":"","label":"Nombre de usuario:", "name":"usuario"},
			{"tipo":"pass","valor":"","label":" Contraseña:", "name":"contraseña"},
			{"tipo":"pass","valor":"","label":"Repetir Contraseña:", "name":"recontraseña"},]
		
		
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarcliente(request):
	usuario = request.POST.get("usuario")
	email = request.POST.get("email")
	password = request.POST.get("contraseña")
	nombre = request.POST.get("nombre")
	apellido = request.POST.get("apellido")
	try:
		user = User.objects.create_user(username=usuario,
			email=email,
			password=password,
			first_name=nombre,
			last_name=apellido)
		cliente = Cliente.objects.create(usuario=user,
			telefono=request.POST.get("telefono"),
			colonia=request.POST.get("colonia"),
			calle=request.POST.get("calle"),
			no_exterior=request.POST.get("no_exterior"),
			no_interior=request.POST.get("no_interior"),
			ciudad=request.POST.get("ciudad"),
			estado=request.POST.get("estado"),
			pais=request.POST.get("pais"),
			codigopostal=request.POST.get("codigopostal"),)
		return JsonResponse("Correcto", safe=False)
	except Exception as e:
		print(str(e))
		if str(e) == "UNIQUE constraint failed: auth_user.username":
			return JsonResponse("El usuario ya existe", safe=False)
		else:
			return JsonResponse("Verifique sus datos por favor", safe=False)

	
	

@csrf_exempt
def modificarcliente(request):
	if request.POST.get("contraseña") == "" and request.POST.get("recontraseña") == "":
		cliente = Cliente.objects.get(id=request.POST.get("idcliente"))
		cliente.usuario.first_name=request.POST.get("nombre")
		cliente.usuario.last_name=request.POST.get("apellido")
		cliente.usuario.email=request.POST.get("email")
		cliente.telefono = request.POST.get("telefono")
		cliente.colonia=request.POST.get("colonia")
		cliente.calle=request.POST.get("calle")
		cliente.no_exterior=request.POST.get("no_exterior")
		cliente.no_interior=request.POST.get("no_interior")
		cliente.ciudad=request.POST.get("ciudad")
		cliente.estado=request.POST.get("estado")
		cliente.pais=request.POST.get("pais")
		cliente.codigopostal=request.POST.get("codigopostal")
		cliente.usuario.save()
		cliente.save()
		return JsonResponse("Correcto", safe=False)
	else:
		if request.POST.get("contraseña") == request.POST.get("recontraseña"):
			cliente = Cliente.objects.get(id=request.POST.get("idcliente"))
			cliente.usuario.first_name=request.POST.get("nombre")
			cliente.usuario.last_name=request.POST.get("apellido")
			cliente.usuario.email=request.POST.get("email")
			cliente.telefono = request.POST.get("telefono")
			cliente.colonia=request.POST.get("colonia")
			cliente.calle=request.POST.get("calle")
			cliente.no_exterior=request.POST.get("no_exterior")
			cliente.no_interior=request.POST.get("no_interior")
			cliente.ciudad=request.POST.get("ciudad")
			cliente.estado=request.POST.get("estado")
			cliente.pais=request.POST.get("pais")
			cliente.codigopostal=request.POST.get("codigopostal")
			cliente.usuario.set_password(request.POST.get("contraseña"))
			cliente.usuario.save()
			cliente.save()
			return JsonResponse("Correcto", safe=False)
		else:
			return JsonResponse("Incorrecto", safe=False)

@csrf_exempt
def eliminarcliente(request):
	cliente = Cliente.objects.get(id=request.POST.get("id"))
	id = cliente.id
	cliente.usuario.delete()
	cliente.delete()
	return JsonResponse(id, safe=False)