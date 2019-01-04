from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse
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
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import valid_ipn_received
import json
import goslate
import smtplib
import sweetify
import datetime

# @csrf_exempt
# def prueba(request):
# 	ipn = PayPalIPN.objects.last()
	
# 	return JsonResponse(data, safe=False)

@csrf_exempt
def ipn(sender, *args, **kwargs):
	datos = sender
	if datos.payment_status == "Completed":
		num_pedido = Num_Pedido.objects.first()
		data = '{"'+datos.query.replace("&",'","').replace("=",'":"')+'"}'
		data  = json.loads(data)
		email = data["payer_email"].replace("%40","@")
		# usuario = User.objects.get(email=data["payer_email"].replace("%40","@"))
		pedido = Pedido.objects.create(usuario = data["address_name"].replace("+"," "),
			total = datos.mc_gross-datos.mc_fee,
			fecha = datetime.datetime.now(),
			nombre = "Pedido #" + str(num_pedido.pedido-1),
			estado_pedido = "2",
			telefono = "",
			pais = data["address_country"].replace("+"," "),
			estado = data["address_state"].replace("+"," "),
			ciudad = data["address_city"].replace("+"," "),
			direccion = data["address_street"].replace("+"," "),
			codigopostal = data["address_zip"].replace("+"," "),
			email = email,)
		for x in range(int(datos.num_cart_items)-1):
			string = data["item_name"+str(x+1)]
			print('{"'+string.replace("id%3A",'id":"').replace("%2CN%3A",'","N":"').replace("%2CT%3A",'","T":"')+'"}')
			js = json.loads('{"'+string.replace("id%3A",'id":"').replace("%2CN%3A",'","N":"').replace("%2CT%3A",'","T":"')+'"}')
			id = int(js["id"])
			talla = js["T"]
			nombre = js["N"]
			cantidad = int(data["quantity"+str(x+1)])
			producto = Producto.objects.get(id=id)
			Producto_Pedido.objects.create(producto=producto,
				cantidad=cantidad,
				pedido=pedido,
				talla=talla,)
		Venta.objects.create(usuario=data["address_name"].replace("+"," "),
			fecha=datetime.datetime.now(),
			monto=datos.mc_gross-datos.mc_fee,
			pedido=pedido)

			

		# print(json.loads("{"+sender.query.replace("&",",")+"}"))
		# for x in datos:
		# 	print(datos["item_name_"+str(x)])
	return HttpResponse(data)

valid_ipn_received.connect(ipn)

def variables(request):
	# Empresa
	empresa = Empresa.objects.last()
	request.session["logo"] = empresa.logo.url
	request.session["nombreempresa"] = empresa.nombre
	request.session["giro"] = empresa.giro_de_la_empresa
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

def faqs(request):
	cart = Cart(request)
	variables(request)
	faqs = FAQ.objects.all()
	return render(request, 'faqs.html', {"cart":cart,
										"faqs":faqs,
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
			request.POST.get("correo"),
			['riicoo28@gmail.com'],
			fail_silently=False,
		)
	Mensaje.objects.create(nombre = request.POST.get("nombre"),
		asunto = request.POST.get("asunto"),
		email = request.POST.get("correo"),
		mensaje = request.POST.get("mensaje"),
		estado ="Sin leer")
	sweetify.error(request, 'El mensaje ha sido enviado nuestro equipo se pondra en contacto con usted', persistent=':(')
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
	try:
		user = User.objects.create_user(username=usuario,
		email=email,
		password=password,
		first_name=nombre,
		last_name=apellido)
		user = authenticate(request, username=usuario, password=password)

		if request.method == 'GET':
			return redirect("/")
		else:
			# sale = Sale()
			# sale.charge(request, user)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
			else:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	except Exception as e:
		sweetify.error(request, 'El nombre de usuario ya esta en uso', persistent=':(')
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
		sweetify.error(request, 'Usuario o contraseña incorrecto', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def req_sesion(request):
	cart = Cart(request)
	sweetify.error(request, 'Nesecitas iniciar sesion para acceder a esta seccion', persistent=':(')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@csrf_exempt
def recuperarcontraseña(request):
	cart = Cart(request)
	email = request.POST.get("email")
	username = request.POST.get("username")
	if User.objects.filter(email=email).exists():
		user = User.objects.get(email=email)
		datos = Cliente.objects.get(usuario=user)
		datos.token_req = request.POST.get("token")
		datos.save()
		cart = Cart(request)
		send_mail(
			'Recuperar contraseña Leborde',
			'Ingresa al siguiente url para modificar tu contraseña \n http://127.0.0.1:8000/modificarcontra/' + request.POST.get("token"),
			user.email,
			[user.email],
			fail_silently=False,
		)
		sweetify.success(request, 'Nesecitas iniciar sesion para acceder a esta seccion', persistent=':(')
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		datos = Cliente.objects.get(usuario=user)
		datos.token_req = request.POST.get("token")
		datos.save()
		cart = Cart(request)
		send_mail(
			'Recuperar contraseña Leborde',
			'Ingresa al siguiente url para modificar tu contraseña \n http://127.0.0.1:8000/modificarcontra/' + request.POST.get("token"),
			user.email,
			[user.email],
			fail_silently=False,
		)
		sweetify.success(request, 'Se ha enviado un enlace a su correo', persistent=':(')
	else:
		sweetify.error(request, 'El usuario o el correo no existe', persistent=':(')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@csrf_exempt
def modificarcontra(request, token):
	if Cliente.objects.filter(token_req=token).exists():
		return render(request, 'modificarcontra.html', {"token":token,})
	else:
		sweetify.error(request, 'Lo siento el token para modificar contraseña no es valido', persistent=':(')
		return redirect("/")
	

@csrf_exempt
def cambiarpassword(request):
	datos = Cliente.objects.get(token_req=request.POST.get("token"))
	user = datos.usuario
	if request.POST.get("password") == request.POST.get("confirm-password"):
		user.set_password(request.POST.get("password"))
		user.save()
		datos.token_req = ""
		datos.save()
		sweetify.success(request, 'Su contraseña ha sido modificada correctamente', persistent=':(')
		return redirect("/")
	else:
		sweetify.success(request, 'Verifique que sus contraseñas coincidan', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url='/')	
def perfil(request):
	cart = Cart(request)
	variables(request)
	user = request.user
	datos = Cliente.objects.get(usuario=user)
	return render(request, 'datos.html', {"cart":cart, "datos":datos,})

@login_required(login_url='/')	
def modificardatos(request):
	user = request.user
	cliente = Cliente.objects.get(usuario=user)
	cliente.usuario.first_name=request.POST.get("nombre")
	cliente.usuario.last_name=request.POST.get("apellido")
	cliente.usuario.email=request.POST.get("email")
	cliente.telefono = request.POST.get("telefono")
	cliente.direccion=request.POST.get("direccion")
	cliente.ciudad=request.POST.get("ciudad")
	cliente.estado=request.POST.get("estado")
	cliente.pais=request.POST.get("pais")
	cliente.codigopostal=request.POST.get("codigo")
	cliente.usuario.save()
	cliente.save()
	sweetify.success(request, 'Sus datos han sido modificados correctamente', persistent=':(')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url='/')	
def modificarcontraseña(request):
	user = request.user
	cliente = Cliente.objects.get(usuario=user)
	if check_password(request.POST.get("viejacontraseña"), user.password):
		if request.POST.get("nuevacontraseña") == request.POST.get("recontraseña"):
			cliente.usuario.set_password(request.POST.get("nuevacontraseña"))
			cliente.usuario.save()
			user = authenticate(request, username=user, password=request.POST.get("nuevacontraseña"))
			login(request, user)
			sweetify.success(request, 'Su contraseña ha sido modificada correctamente', persistent=':(')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			sweetify.error(request, 'Verifique que su nueva contraseña es igual en los dos campos', persistent=':(')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		sweetify.error(request, 'La contraseña antigua no coincide', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# Compras
@login_required(login_url='/req_sesion/')
def pago(request):
	cart = Cart(request)
	envio = Envio.objects.last()
	variables(request)
	cliente = Cliente.objects.get(usuario=request.user)
	if cliente.telefono != "null" and cliente.direccion != "null" and cliente.ciudad != "null" and cliente.estado != "null" and cliente.pais != "null" and cliente.codigopostal != "null":
		estadodatos = True
	else:
		estadodatos = "No cuenta con datos de envio"
	if cart.count() > 0:
		return render(request, 'pago.html', {"cart":cart, "envio":envio, "total":envio.costo.amount+cart.summary(), "estadodatos":estadodatos})
	else:
		sweetify.error(request, 'Agregue por lo menos un producto al carrito de compras', persistent=':(')
		return redirect("/tienda/")

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

# PAYPAL
def pagadopaypal(request):
	sweetify.success(request, 'El pago se ha completado correctamente, espere su pedido de 3 a 5 dias habiles', persistent=':(')
	return redirect("/")

def errorpagadopaypal(request):
	sweetify.success(request, 'El pago no se a podido completar', persistent=':(')
	return redirect("/")

def pagarpaypal(request):
	envio = Envio.objects.last()
	datos = Cliente.objects.get(usuario=request.user)
	cart = Cart(request)
	suma = cart.summary()+envio.costo.amount
	productos = {}
	cont = 1
	for item in cart:
		productos["item_name_"+str(cont)] = "id:"+ str(item.product.id) + ",N:"+ item.product.nombre + ",T:" + item.talla
		productos["amount_"+str(cont)] = item.unit_price
		productos["quantity_"+str(cont)] = item.quantity			
		cont += 1
	productos["item_name_"+str(cont)] = "Envio"
	productos["amount_"+str(cont)] = ("%.2f" % envio.costo)
	productos["quantity_"+str(cont)] = 1

	pedido = Num_Pedido.objects.first()
	pedido.pedido += 1
	pedido.save()
	# What you want the button to do.
	
	if request.POST.get("enviomod") == "2":
		envio = {"email":request.POST.get("email"),
		"pais":request.POST.get("pais"),
		"ciudad":request.POST.get("ciudad"),
		"estado":request.POST.get("estado"),
		"direccion":request.POST.get("colonia")+" "+request.POST.get("direccion")+ " " + request.POST.get("exterior") + " " + request.POST.get("interior"),
		"codigo":request.POST.get("codigo"),
		"telefono":request.POST.get("telefono"),
		"nombre":request.POST.get("nombrerev")}
		paypal_dict = {
			"business": "riicoo28@gmail.com",
			"receiver_email":"riicoo28@gmail.com",
			"payer_email":request.POST.get("email"),
			"address_override":1,
			"country":"MX",
			"city":request.POST.get("ciudad"),
			"state":request.POST.get("estado"),
			"address1":request.POST.get("colonia")+" "+request.POST.get("direccion")+ " " + request.POST.get("exterior") + " " + request.POST.get("interior") ,
			"zip":request.POST.get("codigo"),
			"contact_phone":request.POST.get("telefono"),
			"first_name":request.POST.get("nombrerev"),
			"cmd":"_cart",
			"upload":1,
			"invoice": pedido.pedido,
			"currency_code":"MXN",
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": request.build_absolute_uri(reverse('pagadopaypal')),
			"cancel_return": request.build_absolute_uri(reverse('errorpagadopaypal')),
		}
	else:
		envio = {"email":request.user.email,
		"pais":datos.pais,
		"ciudad":datos.ciudad,
		"estado":datos.estado,
		"direccion":datos.direccion,
		"codigo":datos.codigopostal,
		"telefono":datos.telefono,
		"nombre":request.user.first_name+" "+request.user.last_name}
		paypal_dict = {
			"business": "riicoo28@gmail.com",
			"receiver_email":"riicoo28@gmail.com",
			"payer_email":request.user.email,
			"address_override":1,
			"country":"MX",
			"city":datos.ciudad,
			"state":datos.estado,
			"address1":datos.direccion,
			"zip":datos.codigopostal,
			"contact_phone":datos.telefono,
			"first_name":request.user.first_name+" "+request.user.last_name,
			"cmd":"_cart",
			"upload":1,
			"invoice": pedido.pedido,
			"currency_code":"MXN",
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": request.build_absolute_uri(reverse('pagadopaypal')),
			"cancel_return": request.build_absolute_uri(reverse('errorpagadopaypal')),
		}
	dic = paypal_dict.update(productos)
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form, "cart":cart, "denvio":envio, "envio":Envio.objects.last(), "suma":("%.2f" % suma), "total":Envio.objects.last().costo.amount+cart.summary(),}
	return render(request, "pagopaypal.html", context)