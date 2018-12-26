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
from .import forms
import sweetify
import operator
import json
import collections

# Create your views here.
def index(request):
	año = datetime.now(tz=timezone.utc)
	ventas = Venta.objects.filter(fecha__month=año.month)
	sumapedidos = Pedido.objects.filter(fecha__month=año.month)
	productos_mas = Producto_Pedido.objects.all().order_by("producto")
	sumascantidades = {}
	productoen2 = ""
	for producto in productos_mas:
		productoen = producto.producto
		if productoen == productoen2:
			sumascantidades[producto.producto.id] = sumascantidades[producto.producto.id] + producto.cantidad
		else:
			sumascantidades[producto.producto.id] = producto.cantidad
			productoen2 = producto.producto

	maspedidos = {"1":"","2":"","3":"","4":"","5":""}
	if len(sumascantidades) > 0:
		maximo = max(sumascantidades.items(), key=operator.itemgetter(1))[0]
		maspedidos["1"] = Producto.objects.get(id = maximo)
		del sumascantidades[maximo]
	if len(sumascantidades) > 1:
		maximo = max(sumascantidades.items(), key=operator.itemgetter(1))[0]
		maspedidos["2"] = Producto.objects.get(id = maximo)
		del sumascantidades[maximo]
	if len(sumascantidades) > 2:
		maximo = max(sumascantidades.items(), key=operator.itemgetter(1))[0]
		maspedidos["3"] = Producto.objects.get(id = maximo)
		del sumascantidades[maximo]
	if len(sumascantidades) > 3:
		maximo = max(sumascantidades.items(), key=operator.itemgetter(1))[0]
		maspedidos["4"] = Producto.objects.get(id = maximo)
		del sumascantidades[maximo]
	if len(sumascantidades) > 4:
		maximo = max(sumascantidades.items(), key=operator.itemgetter(1))[0]
		maspedidos["5"] = Producto.objects.get(id = maximo)
		del sumascantidades[maximo]

	print(maspedidos)


	sumaventas = 0
	for venta in ventas:
		sumaventas += venta.monto.amount

	ultimospedidos = Pedido.objects.all()[:5]
	return render(request, "admin.html", {"ventas":sumaventas, "sumapedidos":len(sumapedidos), "maspedidos":maspedidos, "ultimospedidos":ultimospedidos})