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
# Ventas
def semana(date):
	year, week, dow = date.isocalendar()
	if dow == 7:
		start_date = date - timedelta(days=1)
	else:
		start_date = date - timedelta(dow) + timedelta(days=1)
	end_date = start_date + timedelta(6)
	return (start_date, end_date)

def semanaantes(date, multi):
	dias = 7*multi
	date = date - timedelta(days=dias)
	year, week, dow = date.isocalendar()
	if dow == 7:
		start_date = date - timedelta(days=1)
	else:
		start_date = date - timedelta(dow) + timedelta(days=1)
	end_date = start_date + timedelta(6)
	return (start_date, end_date)

def semanasiguiente(date, multi):
	dias = 7*multi
	date = date + timedelta(days=dias)
	year, week, dow = date.isocalendar()
	if dow == 7:
		start_date = date - timedelta(days=1)
	else:
		start_date = date - timedelta(dow) + timedelta(days=1)
	end_date = start_date + timedelta(6)
	return (start_date, end_date)
	
@csrf_exempt
def showventas(request):
	week = (semana(datetime.now(tz=timezone.utc)))
	ventas = Venta.objects.filter(fecha__range=week)
	listaventas = {"lunes":0,
		"martes":0,
		"miercoles":0,
		"jueves":0,
		"viernes":0,
		"sabado":0,
		"domingo":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%A") == "Monday":
			listaventas["lunes"] = listaventas["lunes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Tuesday":
			listaventas["martes"] = listaventas["martes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Wednesday":
			listaventas["miercoles"] = listaventas["miercoles"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Thursday":
			listaventas["jueves"] = listaventas["jueves"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Friday":
			listaventas["viernes"] = listaventas["viernes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Saturday":
			listaventas["sabado"] = listaventas["sabado"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Sunday":
			listaventas["domingo"] = listaventas["domingo"] + venta.monto.amount
	
		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	
	
	data = {"ventas":listaventas, "semana":week[0].strftime("%d/%m/%y") + " - " + week[1].strftime("%d/%m/%y"), "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showventasanterior(request):
	week = (semanaantes(datetime.now(tz=timezone.utc), int(request.POST.get("multiplicador"))))
	ventas = Venta.objects.filter(fecha__range=week)
	listaventas = {"lunes":0,
		"martes":0,
		"miercoles":0,
		"jueves":0,
		"viernes":0,
		"sabado":0,
		"domingo":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%A") == "Monday":
			listaventas["lunes"] = listaventas["lunes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Tuesday":
			listaventas["martes"] = listaventas["martes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Wednesday":
			listaventas["miercoles"] = listaventas["miercoles"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Thursday":
			listaventas["jueves"] = listaventas["jueves"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Friday":
			listaventas["viernes"] = listaventas["viernes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Saturday":
			listaventas["sabado"] = listaventas["sabado"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Sunday":
			listaventas["domingo"] = listaventas["domingo"] + venta.monto.amount

		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	
	data = {"ventas":listaventas, "semana":week[0].strftime("%d/%m/%y") + " - " + week[1].strftime("%d/%m/%y"), "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showventassiguiente(request):
	week = (semanasiguiente(datetime.now(tz=timezone.utc), int(request.POST.get("multiplicador"))))
	ventas = Venta.objects.filter(fecha__range=week)
	listaventas = {"lunes":0,
		"martes":0,
		"miercoles":0,
		"jueves":0,
		"viernes":0,
		"sabado":0,
		"domingo":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%A") == "Monday":
			listaventas["lunes"] = listaventas["lunes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Tuesday":
			listaventas["martes"] = listaventas["martes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Wednesday":
			listaventas["miercoles"] = listaventas["miercoles"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Thursday":
			listaventas["jueves"] = listaventas["jueves"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Friday":
			listaventas["viernes"] = listaventas["viernes"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Saturday":
			listaventas["sabado"] = listaventas["sabado"] + venta.monto.amount
		if venta.fecha.strftime("%A") == "Sunday":
			listaventas["domingo"] = listaventas["domingo"] + venta.monto.amount

		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	
	data = {"ventas":listaventas, "semana":week[0].strftime("%d/%m/%y") + " - " + week[1].strftime("%d/%m/%y"), "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)


# Mes
@csrf_exempt
def showventasmensual(request):
	año = datetime.now(tz=timezone.utc)
	ventas = Venta.objects.filter(fecha__year=año.year)
	listaventas = {"enero":0,
		"febrero":0,
		"marzo":0,
		"abril":0,
		"mayo":0,
		"junio":0,
		"julio":0,
		"agosto":0,
		"septiembre":0,
		"octubre":0,
		"noviembre":0,
		"diciembre":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%m") == "01":
			listaventas["enero"] = listaventas["enero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "02":
			listaventas["febrero"] = listaventas["febrero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "03":
			listaventas["marzo"] = listaventas["marzo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "04":
			listaventas["abril"] = listaventas["abril"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "05":
			listaventas["mayo"] = listaventas["mayo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "06":
			listaventas["junio"] = listaventas["junio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "07":
			listaventas["julio"] = listaventas["julio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "08":
			listaventas["agosto"] = listaventas["agosto"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "09":
			listaventas["septiembre"] = listaventas["septiembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "10":
			listaventas["octubre"] = listaventas["octubre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "11":
			listaventas["noviembre"] = listaventas["noviembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "12":
			listaventas["diciembre"] = listaventas["diciembre"] + venta.monto.amount

		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	data = {"ventas":listaventas, "año":año.year, "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showventasanteriormes(request):
	año = datetime.now(tz=timezone.utc)
	año = año.year - int(request.POST.get("multiplicador"))
	ventas = Venta.objects.filter(fecha__year=año)
	listaventas = {"enero":0,
		"febrero":0,
		"marzo":0,
		"abril":0,
		"mayo":0,
		"junio":0,
		"julio":0,
		"agosto":0,
		"septiembre":0,
		"octubre":0,
		"noviembre":0,
		"diciembre":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%m") == "01":
			listaventas["enero"] = listaventas["enero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "02":
			listaventas["febrero"] = listaventas["febrero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "03":
			listaventas["marzo"] = listaventas["marzo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "04":
			listaventas["abril"] = listaventas["abril"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "05":
			listaventas["mayo"] = listaventas["mayo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "06":
			listaventas["junio"] = listaventas["junio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "07":
			listaventas["julio"] = listaventas["julio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "08":
			listaventas["agosto"] = listaventas["agosto"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "09":
			listaventas["septiembre"] = listaventas["septiembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "10":
			listaventas["octubre"] = listaventas["octubre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "11":
			listaventas["noviembre"] = listaventas["noviembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "12":
			listaventas["diciembre"] = listaventas["diciembre"] + venta.monto.amount

		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	data = {"ventas":listaventas, "año":año, "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showventassiguientemes(request):
	año = datetime.now(tz=timezone.utc)
	año = año.year + int(request.POST.get("multiplicador"))
	ventas = Venta.objects.filter(fecha__year=año)
	listaventas = {"enero":0,
		"febrero":0,
		"marzo":0,
		"abril":0,
		"mayo":0,
		"junio":0,
		"julio":0,
		"agosto":0,
		"septiembre":0,
		"octubre":0,
		"noviembre":0,
		"diciembre":0,}
	listventas = {}
	totalventas = 0
	for venta in ventas:
		if venta.fecha.strftime("%m") == "01":
			listaventas["enero"] = listaventas["enero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "02":
			listaventas["febrero"] = listaventas["febrero"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "03":
			listaventas["marzo"] = listaventas["marzo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "04":
			listaventas["abril"] = listaventas["abril"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "05":
			listaventas["mayo"] = listaventas["mayo"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "06":
			listaventas["junio"] = listaventas["junio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "07":
			listaventas["julio"] = listaventas["julio"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "08":
			listaventas["agosto"] = listaventas["agosto"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "09":
			listaventas["septiembre"] = listaventas["septiembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "10":
			listaventas["octubre"] = listaventas["octubre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "11":
			listaventas["noviembre"] = listaventas["noviembre"] + venta.monto.amount
		if venta.fecha.strftime("%m") == "12":
			listaventas["diciembre"] = listaventas["diciembre"] + venta.monto.amount

		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	data = {"ventas":listaventas, "año":año, "listaventas":listventas, "totalventas":totalventas}
	return JsonResponse(data, safe=False)

# Rango de Fechas
# Mes
@csrf_exempt
def showventasrange(request):
	año = datetime.now(tz=timezone.utc)
	inicio = request.POST.get("inicio")
	final = request.POST.get("final")
	inicio = datetime.strptime(str(inicio).replace("-"," "), '%Y %m %d')
	final = datetime.strptime(str(final).replace("-"," "), '%Y %m %d')
	ventas = Venta.objects.filter(fecha__range=[inicio,final])
	totalventas = 0
	arraydates = []
	ventasfechas = {}
	listventas = {}
	date_generated = [inicio + timedelta(days=x) for x in range(0, (final-inicio).days)]
	for d in date_generated:
		ventasfechas[d.strftime("%d-%m-%Y")] = 0
		arraydates.append(d.strftime("%d-%m-%Y"))
	for venta in ventas:
		for x,y in ventasfechas.items():
			if venta.fecha.strftime("%d-%m-%Y") == x:
				ventasfechas[x] = y+venta.monto.amount
		listventas[venta.id] = {"id":venta.id,
			"nombre":venta.usuario.first_name + " " + venta.usuario.last_name,
			"fecha":venta.fecha,
			"total":venta.monto.amount}
		totalventas += venta.monto.amount
	data = {"ventas":ventasfechas, "listaventas":listventas, "año":año.year, "totalventas":totalventas,"fechas":arraydates}
	return JsonResponse(data, safe=False)