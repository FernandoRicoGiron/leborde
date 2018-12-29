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
	colecciones = Coleccion.objects.all()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones
										})

def categoria(request, id):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	categoria = Categoria.objects.get(id=id)
	productos = Producto.objects.filter(categoria=categoria)
	colecciones = Coleccion.objects.all()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones
										})

def coleccion(request, id):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	coleccion = Coleccion.objects.get(id=id)
	productos = coleccion.productos.all()
	colecciones = Coleccion.objects.all()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones
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

def contacto(request):
	cart = Cart(request)
	variables(request)
	empresa = Empresa.objects.last()
	return render(request, 'contacto.html', {"cart":cart,
										"empresa":empresa
										})

def mensajecontacto(request):
	send_mail(
			'Contacto Leborde ' + request.POST.get("asunto"),
			'La persona '+ request.POST.get("nombre") + ' con el correo '+request.POST.get("correo") + " desea saber la siguiente informacion:\n" + request.POST.get("asunto") + '\n' +request.POST.get("mensaje"),
			request.POST.get("email"),
			['riicoo28@gmail.com'],
			fail_silently=False,
		)
	return redirect("/contacto/")

# Autentificacion
@csrf_exempt
def registrar(request):
	cart = Cart(request)
	usuario = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	nombre = request.POST.get("nombre")
	apellido = request.POST.get("apellido")
	user = User.objects.create_user(username=usuario,
		email=email,
		password=password,
		first_name=nombre,
		last_name=apellido)
	user = authenticate(request, username=usuario, password=password)

	if request.method == 'GET':
		return redirect("/")
	else:
		sale = Sale()
		sale.charge(request, user)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	

@csrf_exempt
def cerrarsesion(request):
	logout(request)
	cart = Cart(request)
	return redirect("/")

@csrf_exempt
def iniciarsesion(request):
	cart = Cart(request)
	usuario = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	user = authenticate(request, username=usuario, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def req_sesion(request):
	cart = Cart(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@csrf_exempt
def recuperarcontraseña(request):
	cart = Cart(request)
	email = request.POST.get("email")
	username = request.POST.get("username")
	if User.objects.filter(email=email, username=username).exists():
		user = User.objects.get(email=email, username=username)
		datos = Cliente.objects.get(user=user)
		datos.token_req = request.POST.get("token")
		datos.save()
		cart = Cart(request)
		email = EmailMessage('Recuperar Contraseña', 'Ingresa al siguiente url para modificar tu contraseña \n http://127.0.0.1:8000/modificarcontra/' + request.POST.get("token"),to = [request.POST.get("email")])
		email.send()
		error = False
	else:
		error = True
	return render(request, 'envioderecu.html', {"cart":cart, "errorusu":error,})

@csrf_exempt
def modificarcontra(request, token):
	if Cliente.objects.filter(token_req=token).exists():
		error = False
	else:
		error = True
	return render(request, 'modificarcontra.html', {"error":error,"token":token,})

@csrf_exempt
def cambiarpassword(request):
	datos = Cliente.objects.get(token_req=request.POST.get("token"))
	user = datos.user
	user.set_password(request.POST.get("password"))
	user.save()
	datos.token_req = ""
	datos.save()
	return render(request, 'modificadacontra.html', {})

# Compras
@csrf_exempt
def add_to_cart(request):
	cantidad = request.POST.get("cantidad")
	id = request.POST.get("producto")
	producto = Producto.objects.get(id=id)
	cart = Cart(request)
	talla = Talla.objects.get(id=request.POST.get("talla"))
	cart.add(producto, producto.precio.amount, talla.nombre, cantidad)
	for item in cart:
		if item.product == producto:
			cantidad = item.quantity
	data = {"id":producto.id, "cantidad":cantidad, "suma":cart.summary(), "talla":talla.nombre}
	return JsonResponse(data, safe=False)

@csrf_exempt
def remove_from_cart(request):
	id = request.POST.get("producto")
	producto = Producto.objects.get(id=id)
	cart = Cart(request)
	cantidad = 0
	talla = request.POST.get("talla")
	for item in cart:
		if item.product == producto and item.talla == talla:
			cantidad = item.quantity
	cart.remove(producto, talla)
	data = {"suma":cart.summary(),"id":producto.id, "cantidad":cantidad}
	return JsonResponse(data, safe=False)