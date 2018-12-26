from django.shortcuts import render, render_to_response, redirect
from django.utils import timezone
from .models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.core.mail import EmailMessage
from .utileria import render_pdf
from django.conf import settings
from django.core import serializers
from django.contrib.auth.hashers import check_password
import json
import goslate
import smtplib
import sweetify
import datetime

def variables(request):
	# Empresa
	empresa = Empresa.objects.last()
	request.session["logo"] = empresa.logo.url
	request.session["nombreempresa"] = empresa.nombre
	# Categorias
	categorias = Categoria.objects.all()
	lista = {}
	for categoria in categorias:
		lista[categoria.id] = categoria.nombre
	request.session["categorias"] = lista
	return request

def index(request):
	cart = Cart(request)
	variables(request)
	marcas = Marca.objects.all()
	tipos = Categoria.objects.all()
	populares = Producto.objects.filter(popular=True)
	nuevos = Producto.objects.all().order_by("-id")[:10]
	colecciones = Coleccion.objects.all()
	categorias = Categoria.objects.all()
	# ofertas = Producto.objects.filter(Oferta = True)
	carruseles = Carrusel.objects.all()
	return render(request, 'index.html', {"cart":cart,
										"categorias":categorias,
										"carruseles":carruseles,
										"marcas":marcas,
										"tipos":tipos,
										"populares":populares,
										"nuevos":nuevos,
										"colecciones":colecciones,
										"categorias":categorias})

def nosotros(request):
	cart = Cart(request)
	variables(request)
	empresa = Empresa.objects.last()
	return render(request, 'nosotros.html', {"cart":cart,
										"empresa":empresa,
										})

def tienda(request):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	productos = Producto.objects.all()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										})

def producto(request, id):
	cart = Cart(request)
	variables(request)
	producto = Producto.objects.get(id=id)
	pro_re = Producto.objects.filter(categoria=producto.categoria)
	return render(request, 'producto.html', {"cart":cart,
										"producto":producto,
										"pro_re":pro_re
										})