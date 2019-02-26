from django.shortcuts import render, redirect
from ecommerce.models import *
from administracion.models import *
from sitio.models import *
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
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

def admin_session(request):
	empresa = Empresa.objects.last()
	return render(request, "login.html", {"empresa":empresa})

def iniciardashboard(request):
	usuario = request.POST.get("usuario")
	password = request.POST.get("contraseña")
	user = authenticate(request, username=usuario, password=password)
	if user is not None and user.is_staff:
		login(request, user)
		return redirect("/dashboard/")
	else:
		sweetify.error(request, 'Usuario o contraseña incorrecto o puede que este usuario no tenga los permisos necesarios para acceder al dashboard', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	

# Create your views here.
@login_required(login_url='/dashboard/admin_session/')
def index(request):
	if request.user.is_staff:
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

		ultimospedidos = Pedido.objects.all().order_by("-id")[:5]
		# Eliminacion de pedidos obsoletos
		hoy = datetime.now()
		pedidos = Pedido.objects.filter(estado_pedido=1)
		for pedido in pedidos:
			if not pedido.comprobante:
				d1 = date(hoy.year,hoy.month,hoy.day)
				d2 = date(pedido.fecha.year,pedido.fecha.month,pedido.fecha.day)
				diferencia = abs(d1 - d2).days
				if diferencia > 3:
					pedidoprod = Producto_Pedido.objects.filter(pedido=pedido)
					for producto in pedidoprod:
						if Talla.objects.filter(nombre=producto.talla).exists():
							talla = Talla.objects.get(nombre=producto.talla)
							if Inventario_Talla.objects.filter(producto=producto.producto, talla=talla).exists():
								inventariotalla = Inventario_Talla.objects.get(producto=producto.producto, talla=talla)
								inventariotalla.cantidad += producto.cantidad
								producto.producto.inventario += producto.cantidad
								inventariotalla.save()
								producto.producto.save()
					pedido.delete()
		return render(request, "admin.html", {"ventas":sumaventas, "sumapedidos":len(sumapedidos), "maspedidos":maspedidos, "ultimospedidos":ultimospedidos})
	else:
		logout(request)
		sweetify.error(request, 'Este usuario no cuenta con los permisos necesarios para acceder a esta sección', persistent=':(')
		return redirect("/dashboard/admin_session/")