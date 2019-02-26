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
import requests
# from __future__ import unicode_literal

# @csrf_exempt
# def prueba(request):
# 	ipn = PayPalIPN.objects.last()
	
# 	return JsonResponse(data, safe=False)

@csrf_exempt
def ipn(sender, *args, **kwargs):
	datos = sender
	if datos.payment_status == "Completed":
		num_pedido = Num_Pedido.objects.first()
		pedido = Pedido.objects.get(nombre = "Pedido #" + str(datos.invoice))
		pedido.total = datos.mc_gross-datos.mc_fee
		pedido.estado_pedido = "2"
		pedido.save()

		productos = Producto_Pedido.objects.filter(pedido=pedido)

		for producto in productos:
			talla = Talla.objects.get(nombre = producto.talla)
			talla = Inventario_Talla.objects.get(producto=producto.producto, talla=talla)
			talla.cantidad -= producto.cantidad
			talla.save()
			pro = producto
			pro.inventario -= x.quantity
			pro.save()
		
		Venta.objects.create(usuario=pedido.usuario,
			fecha=datetime.datetime.now(),
			monto=datos.mc_gross-datos.mc_fee,
			pedido=pedido)

		empresa = Empresa.objects.last()
		if empresa.link_encuesta:
			send_mail(
				'Encuesta de servicio '+empresa.nombre,
				'Gracias por comprar en '+empresa.nombre+" su pago se ha completado correctamente, le agradeceriamos que se tome un momento de su tiempo para llenar la siguiente encuesta\n\n"+empresa.link_encuesta,
				empresa.correo,
				[pedido.email],
				fail_silently=False,
			)
		else:
			send_mail(
					'Graias de parte de '+empresa.nombre,
					'Gracias por comprar en '+empresa.nombre+" su pago se ha completado correctamente, ",
					empresa.correo,
					[pedido.email],
					fail_silently=False,
				)

		# print(json.loads("{"+sender.query.replace("&",",")+"}"))
		# for x in datos:
		# 	print(datos["item_name_"+str(x)])
	return HttpResponse("correcto")

valid_ipn_received.connect(ipn)

def variables(request):
	# Empresa
	empresa = Empresa.objects.last()
	request.session["logo"] = empresa.logo.url
	request.session["nombreempresa"] = empresa.nombre
	request.session["giro"] = empresa.giro_de_la_empresa
	request.session["titulo"] = empresa.titulo
	# redes sociales
	request.session["facebook"] = empresa.facebook
	request.session["twiter"] = empresa.twiter
	request.session["instagram"] = empresa.instagram
	request.session["youtube"] = empresa.youtube
	# Categorias
	categorias = Categoria.objects.all()
	marcas = Marca.objects.all()
	lista = {}
	for categoria in categorias:
		lista[categoria.id] = categoria.nombre
	request.session["categorias"] = lista

	lista = {}
	for marca in marcas:
		lista[marca.id] = {"nombre":marca.nombre, "imagen":marca.imagen.url}
	request.session["marcas"] = lista
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
	seccion = Secciones.objects.last()
	quienessomos = QuienesSomos.objects.all()
	return render(request, 'nosotros.html', {"cart":cart,
										"empresa":empresa,
										"seccion":{"titulo":seccion.tituloqs, "imagen":seccion.imagenqs.url},
										"quienessomos":quienessomos
										})

def faqs(request):
	cart = Cart(request)
	variables(request)
	faqs = FAQ.objects.all()
	seccion = Secciones.objects.last()
	return render(request, 'faqs.html', {"cart":cart,
										"faqs":faqs,
										"seccion":{"titulo":seccion.titulopreguntas, "imagen":seccion.imagenpreguntas.url}
										})

def tienda(request):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	productos = Producto.objects.filter(en_tienda=True)
	colecciones = Coleccion.objects.all()
	seccion = Secciones.objects.last()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones,
										"seccion":{"titulo":seccion.titulot, "imagen":seccion.imagent.url}
										})

def categoria(request, id):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	categoria = Categoria.objects.get(id=id)
	productos = Producto.objects.filter(categoria=categoria, en_tienda=True)
	colecciones = Coleccion.objects.all()
	seccion = Secciones.objects.last()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones,
										"seccion":{"titulo":seccion.titulot, "imagen":seccion.imagent.url}
										})

def coleccion(request, id):
	cart = Cart(request)
	variables(request)
	categorias = Categoria.objects.all()
	coleccion = Coleccion.objects.get(id=id)
	productos = coleccion.productos.filter(en_tienda=True)
	colecciones = Coleccion.objects.all()
	seccion = Secciones.objects.last()
	return render(request, 'tienda.html', {"cart":cart,
										"categorias":categorias,
										"productos":productos,
										"colecciones":colecciones,
										"seccion":{"titulo":seccion.titulot, "imagen":seccion.imagent.url},
										"coleccion":coleccion,
										})

def producto(request, id):
	empresa = Empresa.objects.last()
	cart = Cart(request)
	variables(request)
	producto = Producto.objects.get(id=id)
	tallas_prod = Inventario_Talla.objects.filter(producto=producto)
	pro_re = Producto.objects.filter(categoria=producto.categoria)
	envio = Envio.objects.last()
	estadodatos = False
	if request.user.is_authenticated:
		cliente = Cliente.objects.get(usuario=request.user)
		if cliente.telefono != "null" and cliente.calle != "null" and cliente.colonia != "null" and cliente.no_exterior != "null" and cliente.ciudad != "null" and cliente.estado != "null" and cliente.pais != "null" and cliente.codigopostal != "null":
			estadodatos = True
		else:
			estadodatos = "No cuenta con datos de envio"
	return render(request, 'producto.html', {"cart":cart,
										"producto":producto,
										"pro_re":pro_re,
										"envio":envio.costo.amount,
										"estadodatos":estadodatos,
										"tallas":tallas_prod,
										"empresa":empresa
										})
@csrf_exempt
def checktalla(request):
	talla = Talla.objects.get(id = request.POST.get("talla"))
	producto = Producto.objects.get(id=request.POST.get("producto"))
	talla = Inventario_Talla.objects.get(producto=producto, talla=talla)
	return JsonResponse(talla.cantidad, safe=False)

def contacto(request):
	cart = Cart(request)
	variables(request)
	empresa = Empresa.objects.last()
	seccion = Secciones.objects.last()
	return render(request, 'contacto.html', {"cart":cart,
										"empresa":empresa,
										"seccion":{"titulo":seccion.tituloc, "imagen":seccion.imagenc.url}
										})

def mensajecontacto(request):
	empresa = Empresa.objects.last()
	send_mail(
			'Contacto ' + empresa.nombre +' ' + request.POST.get("asunto"),
			'La persona '+ request.POST.get("nombre") + ' con el correo '+request.POST.get("correo") + " y numero de telefono: "+request.POST.get("telefono")+" desea saber la siguiente informacion:\n" + request.POST.get("asunto") + '\n' +request.POST.get("mensaje"),
			request.POST.get("correo"),
			[empresa.correo],
			fail_silently=False,
		)
	Mensaje.objects.create(nombre = request.POST.get("nombre"),
		asunto = request.POST.get("asunto"),
		email = request.POST.get("correo"),
		mensaje = request.POST.get("mensaje"),
		telefono = request.POST.get("telefono"),
		estado ="Sin leer")
	sweetify.error(request, 'El mensaje ha sido enviado nuestro equipo se pondrá en contacto con usted', persistent=':(')
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
	if User.objects.filter(email=email).exists():
		sweetify.error(request, 'Ya existe un usuario on este correo', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
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
	empresa = Empresa.objects.last()
	cart = Cart(request)
	email = request.POST.get("email")
	username = request.POST.get("username")
	if email != "" or username != "":
		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			datos = Cliente.objects.get(usuario=user)
			datos.token_req = request.POST.get("token")
			datos.save()
			cart = Cart(request)
			send_mail(
				'Recuperar contraseña Leborde',
				'Ingresa al siguiente url para modificar tu contraseña \n http://istmeña.com/modificarcontra/' + request.POST.get("token"),
				empresa.correo,
				[user.email],
				fail_silently=False,
			)
			sweetify.success(request, 'Se ha enviado un enlace a su correo', persistent=':(')
		elif User.objects.filter(username=username).exists():
			user = User.objects.get(username=username)
			datos = Cliente.objects.get(usuario=user)
			datos.token_req = request.POST.get("token")
			datos.save()
			cart = Cart(request)
			send_mail(
				'Recuperar contraseña Leborde',
				'Ingresa al siguiente url para modificar tu contraseña \n http://istmeña.com/modificarcontra/' + request.POST.get("token"),
				empresa.correo,
				[user.email],
				fail_silently=False,
			)
			sweetify.success(request, 'Se ha enviado un enlace a su correo', persistent=':(')
		else:
			sweetify.error(request, 'El usuario o el correo no existe', persistent=':(')
	else:
		sweetify.error(request, 'Ingrese un usuario o un email por favor', persistent=':(')
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
	seccion = Secciones.objects.last()
	colonias = {}
	if datos.codigopostal:
		colonias = requests.get('https://api-codigos-postales.herokuapp.com/v2/codigo_postal/'+datos.codigopostal)
		colonias = colonias.json(),
	return render(request, 'datos.html', {"cart":cart,
		"datos":datos,
		"seccion":{"titulo":seccion.titulop, "imagen":seccion.imagenp.url},
		"colonias": colonias
		})

@login_required(login_url='/')	
def modificardatos(request):
	user = request.user
	cliente = Cliente.objects.get(usuario=user)
	cliente.usuario.first_name=request.POST.get("nombre")
	cliente.usuario.last_name=request.POST.get("apellido")
	cliente.usuario.email=request.POST.get("email")
	cliente.telefono = request.POST.get("telefono")
	cliente.colonia=request.POST.get("colonia")
	cliente.calle=request.POST.get("calle")
	cliente.no_exterior=request.POST.get("exterior")
	cliente.no_interior=request.POST.get("interior")
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
	print(cliente.telefono)
	if cliente.telefono != None and cliente.colonia != None and cliente.calle != None and cliente.no_exterior != None and cliente.ciudad != None and cliente.estado != None and cliente.pais != None and cliente.codigopostal != None:
		estadodatos = True
	else:
		estadodatos = "No cuenta con datos de envio"
	if cart.count() > 0:
		seccion = Secciones.objects.last()
		return render(request, 'pago.html', {"cart":cart, "seccion":{"titulo":seccion.titulodp, "imagen":seccion.imagendp.url}, "envio":envio, "total":envio.costo.amount+cart.summary(), "estadodatos":estadodatos, "cliente":cliente})
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
	cantidadincart = 0
	for item in cart:
		if item.product == producto and item.talla == talla.nombre:
			cantidadincart = item.quantity

	sumacants = int(cantidad) + int(cantidadincart)

	inventario = Inventario_Talla.objects.get(producto=producto, talla=talla)

	if sumacants <= int(inventario.cantidad):
		# print(producto.inventario)
		# print((int(cantidad) + int(cantidadincart)))
		cart.add(producto, producto.precio.amount, talla.nombre, cantidad)
		for item in cart:
			if item.product == producto and item.talla == talla.nombre:
				cantidad = item.quantity
		data = {"id":producto.id, "cantidad":cantidad, "suma":cart.summary(), "talla":talla.nombre, "tallareplace":talla.nombre.replace(" ","").replace("/","")}
	else:
		data = {"error":"No hay suficientes productos en el inventario"}
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
	data = {"suma":cart.summary(),"id":producto.id, "cantidad":cantidad, "tallareplace":talla.replace(" ","").replace("/","")}
	return JsonResponse(data, safe=False)

@csrf_exempt
def update_to_cart(request):
	cantidad = request.POST.get("cantidad")
	id = request.POST.get("producto")
	producto = Producto.objects.get(id=id)
	cart = Cart(request)
	talla = Talla.objects.get(nombre=request.POST.get("talla"))

	cantidadincart = 0
	for item in cart:
		if item.product == producto and item.talla == talla.nombre:
			cantidadincart = item.quantity

	sumacants = int(cantidad) + int(cantidadincart)

	inventario = Inventario_Talla.objects.get(producto=producto, talla=talla)
	
	if sumacants <= int(inventario.cantidad):
		for item in cart:
			if item.product == producto and item.talla == talla.nombre:
				cantidad = item.quantity
				precio = item.total_price

		cart.update(producto, talla, request.POST.get("cantidad"), producto.precio.amount)
		data = {"suma":cart.summary(),"id":producto.id, "cantidad":cantidad, "precio":precio, "totalproductos":cart.count(), "tallareplace":talla.nombre.replace(" ","").replace("/","")}
	else:
		data = {"error":"No hay suficientes productos en el inventario", "cantidad":int(cantidadincart)}
	return JsonResponse(data, safe=False)

# PAYPAL
def pagadopaypal(request):
	cart = Cart(request)
	cart.clear()
	sweetify.success(request, 'El pago se ha completado correctamente, espere su pedido de 3 a 5 dias habiles', persistent=':(')
	return redirect("/")

def errorpagadopaypal(request):
	sweetify.success(request, 'El pago no se ha podido completar', persistent=':(')
	return redirect("/")

def pagarpaypal(request):
	print(request.POST.get("telefono"))
	empresa = Empresa.objects.last()
	envio = Envio.objects.last()
	datos = Cliente.objects.get(usuario=request.user)
	cart = Cart(request)
	if not request.POST.get("colonia") and request.POST.get("enviomod") == "2":
		sweetify.success(request, 'Verifica que tus datos esten correctos', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	productos = {}
	cont = 1
	for item in cart:
		productos["item_name_"+str(cont)] = "id:"+ str(item.product.id) + ",N:"+ item.product.nombre + ",T:" + item.talla
		productos["amount_"+str(cont)] = item.unit_price
		productos["quantity_"+str(cont)] = item.quantity			
		cont += 1

	productos["item_name_"+str(cont)] = "Envio"
	if request.POST.get("ciudad") != "Tuxtla Gutiérrez":
		productos["amount_"+str(cont)] = ("%.2f" % envio.costo)
		suma = cart.summary()+envio.costo.amount
	else:
		productos["amount_"+str(cont)] = 0.00
		suma = cart.summary()
	productos["quantity_"+str(cont)] = 1

	pedido = Num_Pedido.objects.first()
	pedido.pedido += 1
	pedido.save()
	# What you want the button to do.
	datoscomplete = False
	print(request.POST)
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
			"business": empresa.correopaypal,
			"receiver_email":empresa.correopaypal,
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
		if envio["email"] != "" and envio["pais"] != "" and envio["ciudad"] != "" and envio["estado"] != "" and envio["direccion"] != "" and envio["codigo"] != "" and envio["telefono"] != "" and envio["nombre"] != "":
			pedido = Pedido.objects.create(usuario = request.user,
				total =suma,
				fecha = datetime.datetime.now(),
				nombre = "Pedido #" + str(pedido.pedido),
				estado_pedido = "1",
				telefono = request.POST.get("telefono"),
				pais = request.POST.get("pais"),
				estado = request.POST.get("estado"),
				ciudad = request.POST.get("ciudad"),
				direccion = request.POST.get("colonia") + " " +request.POST.get("direccion") + " " + request.POST.get("exterior") + " " + request.POST.get("interior"),
				codigopostal = request.POST.get("codigo"),
				email = request.POST.get("email"),)
			datoscomplete = True
		
	else:
		envio = {"email":request.user.email,
		"pais":datos.pais,
		"ciudad":datos.ciudad,
		"estado":datos.estado,
		"direccion":datos.colonia + " " + datos.calle + " " +datos.no_exterior + " " + datos.no_interior,
		"codigo":datos.codigopostal,
		"telefono":datos.telefono,
		"nombre":request.user.first_name+" "+request.user.last_name}
		paypal_dict = {
			"business": empresa.correopaypal,
			"receiver_email":empresa.correopaypal,
			"payer_email":request.user.email,
			"address_override":1,
			"country":"MX",
			"city":datos.ciudad,
			"state":datos.estado,
			"address1":datos.colonia + " " + datos.calle + " " +datos.no_exterior + " " + datos.no_interior,
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
		if envio["email"] != "" and envio["pais"] != "" and envio["ciudad"] != "" and envio["estado"] != "" and envio["direccion"] != "" and envio["codigo"] != "" and envio["telefono"] != "" and envio["nombre"] != "":
			pedido = Pedido.objects.create(usuario = request.user,
					total = suma,
					fecha = datetime.datetime.now(),
					nombre = "Pedido #" + str(pedido.pedido),
					estado_pedido = "1",
					telefono = datos.telefono,
					pais = datos.pais,
					estado = datos.estado,
					ciudad = datos.ciudad,
					direccion = datos.colonia + " " + datos.calle + " " +datos.no_exterior + " " + datos.no_interior,
					codigopostal = datos.codigopostal,
					email = request.user.email,)
			datoscomplete = True
	for x in cart:
		Producto_Pedido.objects.create(producto=x.product,
				cantidad=x.quantity,
				pedido=pedido,
				talla=x.talla,)
	dic = paypal_dict.update(productos)
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	seccion = Secciones.objects.last()
	context = {"form": form, "cart":cart, "denvio":envio, "envio":Envio.objects.last(), "suma":("%.2f" % suma), "total":Envio.objects.last().costo.amount+cart.summary(),"seccion":{"titulo":seccion.tituloppaypal, "imagen":seccion.imagenppaypal.url}}
	
	if datoscomplete:

		return render(request, "pagopaypal.html", context)
	else:
		sweetify.success(request, 'Verifica que tus datos esten correctos', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# Pedidos cuando no hay existencia
@login_required(login_url='/req_sesion/')
def pedido(request):
	producto = Producto.objects.get(id=request.POST.get("idprod"))
	cantidad = request.POST.get("cantidad")
	talla = request.POST.get("talla")
	envio = Envio.objects.last()
	num_pedido = Num_Pedido.objects.first()
	num_pedido.pedido += 1
	num_pedido.save()
	total = producto.precio * cantidad
	print(request.POST.get("enviomod"))
	if request.POST.get("enviomod") == "2":
		if request.POST.get("ciudad") != "Tuxtla Gutiérrez":
			total = total + envio.costo
		pedido = Pedido.objects.create(usuario = request.user,
				total = total,
				fecha = datetime.datetime.now(),
				nombre = "Pedido #" + str(num_pedido.pedido),
				estado_pedido = "1",
				telefono = request.POST.get("telefono"),
				pais = request.POST.get("pais"),
				estado = request.POST.get("estado"),
				ciudad = request.POST.get("ciudad"),
				direccion = request.POST.get("colonia") + " " +request.POST.get("direccion") + " " + request.POST.get("exterior") + " " + request.POST.get("interior"),
				codigopostal = request.POST.get("codigo"),
				email = request.POST.get("email"),)
	else:
		cliente = Cliente.objects.get(usuario = request.user)
		if cliente.ciudad != "Tuxtla Gutiérrez":
			total = total + envio.costo
		pedido = Pedido.objects.create(usuario = request.user,
				total = total,
				fecha = datetime.datetime.now(),
				nombre = "Pedido #" + str(num_pedido.pedido),
				estado_pedido = "1",
				telefono = cliente.telefono,
				pais = cliente.pais,
				estado = cliente.estado,
				ciudad = cliente.ciudad,
				direccion = cliente.colonia + " " + cliente.calle + " " +cliente.no_exterior + " " + cliente.no_interior,
				codigopostal = cliente.codigopostal,
				email = request.user.email,)

	Producto_Pedido.objects.create(producto=producto,
				cantidad=cantidad,
				pedido=pedido,
				talla=talla,)
	plan = "Total a pagar"
	precio = total
	logo = Empresa.objects.last()
	coenvio = envio.costo.amount
	if request.POST.get("ciudad") == "Tuxtla Gutiérrez":
		coenvio = 0.00
	cart = {"1":{"nombre":producto.nombre,
				"precio":producto.precio.amount,
				"cantidad":cantidad,
				"talla":talla,
				"total":producto.precio * cantidad,
				"imagen":producto.imagenes.first().imagen.url},
				"2":{"nombre":"Envio",
				"precio":coenvio,
				"cantidad":1,
				"talla":"",
				"total":coenvio,
				"imagen":""}}
	empresa = Empresa.objects.last()
	pdf= render_pdf("pagos.html",{"empresa":empresa,"plan":plan, "precio":precio, "logo":logo.logo.url, "ncuenta":logo.numero_de_cuenta, "cart":cart})
	return HttpResponse(pdf,content_type="application/pdf")

def pedido2(request):
	if not request.POST.get("colonia") and request.POST.get("enviomod") == "2":
		sweetify.success(request, 'Verifica que tus datos esten correctos', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	cart = Cart(request)
	if cart.count() > 0:
		cantidad = request.POST.get("cantidad")
		talla = request.POST.get("talla")
		envio = Envio.objects.last()
		num_pedido = Num_Pedido.objects.first()
		num_pedido.pedido += 1
		num_pedido.save()
		
		arreglo = {}
		cont = 1
		total = 0
		for x in cart:
			total += x.total_price
			

		if request.POST.get("enviomod") == "2":
			ciudad = request.POST.get("ciudad")
			if request.POST.get("ciudad") != "Tuxtla Gutiérrez":
				total = total + envio.costo.amount
			pedido = Pedido.objects.create(usuario = request.user,
					total = total,
					fecha = datetime.datetime.now(),
					nombre = "Pedido #" + str(num_pedido.pedido),
					estado_pedido = "1",
					telefono = request.POST.get("telefono"),
					pais = request.POST.get("pais"),
					estado = request.POST.get("estado"),
					ciudad = request.POST.get("ciudad"),
					direccion = request.POST.get("colonia") + " " +request.POST.get("direccion") + " " + request.POST.get("exterior") + " " + request.POST.get("interior"),
					codigopostal = request.POST.get("codigo"),
					email = request.POST.get("email"),)
		else:
			
			cliente = Cliente.objects.get(usuario = request.user)
			ciudad = cliente.ciudad
			if ciudad != "Tuxtla Gutiérrez":
				total = total + envio.costo.amount
			pedido = Pedido.objects.create(usuario = request.user,
					total = total,
					fecha = datetime.datetime.now(),
					nombre = "Pedido #" + str(num_pedido.pedido),
					estado_pedido = "1",
					telefono = cliente.telefono,
					pais = cliente.pais,
					estado = cliente.estado,
					ciudad = cliente.ciudad,
					direccion = cliente.colonia + " " + cliente.calle + " " +cliente.no_exterior + " " + cliente.no_interior,
					codigopostal = cliente.codigopostal,
					email = request.user.email,)

		for x in cart:
			Producto_Pedido.objects.create(producto=x.product,
					cantidad=x.quantity,
					pedido=pedido,
					talla=x.talla,)
			talla = Talla.objects.get(nombre = x.talla)
			invtalla = Inventario_Talla.objects.get(producto=x.product, talla=talla)
			pro = x.product
			pro.inventario -= x.quantity
			invtalla.cantidad -= x.quantity
			pro.save()
			invtalla.save()
			arreglo[cont] = {"nombre":x.product.nombre,
				"precio":x.product.precio.amount,
				"cantidad":x.quantity,
				"talla":x.talla,
				"total":x.total_price,
				"imagen":x.product.imagenes.first().imagen.url}
			cont += 1
		coenvio = envio.costo.amount
		if ciudad == "Tuxtla Gutiérrez":
			coenvio = 0.00
		arreglo[cont] = {"nombre":"Envio",
				"precio":coenvio,
				"cantidad":1,
				"talla":"",
				"total":coenvio,
				"imagen":""}

		plan = "Total a pagar"
		precio = total
		logo = Empresa.objects.last()
		cart.clear()
		empresa = Empresa.objects.last()
		pdf= render_pdf("pagos.html",{"empresa":empresa,"plan":plan, "precio":precio, "logo":logo.logo.url, "ncuenta":logo.numero_de_cuenta, "cart":arreglo})
		email = EmailMessage('Tu pedido en '+empresa.nombre, 'Completa tu pago.', empresa.correo, [request.user.email]) 
		email.attach('pedido'+empresa.nombre+'.pdf', pdf.getvalue() , 'application/pdf') 
		email.send()
		send_mail(
			'Nuevo pedido '+ producto.nombre +' ' + empresa.nombre ,
			'El usuario '+request.user.username+' ha realizado un nuevo pedido ',
			empresa.correo,
			[empresa.correo],
			fail_silently=False,
		)
		return HttpResponse(pdf,content_type="application/pdf")
	else:
		return redirect("/pagar/")

def listapedidos(request):
	cart = Cart(request)
	variables(request)
	pedidos = Pedido.objects.filter(usuario=request.user).order_by("-id")
	seccion = Secciones.objects.last()
	return render(request, 'pedidos.html', {"cart":cart,
		"pedidos":pedidos,
		"seccion":{"titulo":seccion.titulopedidos, "imagen":seccion.imagenpedidos.url}})

def subircomprobante(request, id):
	if "mi-archivo" in request.FILES:
		pedido = Pedido.objects.get(id=id)
		pedido.comprobante = request.FILES["mi-archivo"]
		pedido.save()
		empresa = Empresa.objects.last()
		send_mail(
			'Comprobante de pago '+empresa.nombre,
			'El usuario '+request.user.username+' ha subido el comprobante de pago del pedido numero '+str(pedido.id),
			empresa.correo,
			[empresa.correo],
			fail_silently=False,
		)
		send_mail(
			'Tu comprobante fue recibido con éxito.',
			'Gracias por tu compra, si todo está correcto tu pedido llegará de 3 a 5 días hábiles, si tienes alguna duda o consulta puedes realizarla al WhatsApp de servicio '+empresa.telefono+' ó enviar un correo a: '+empresa.correo+', será un placer atenderle\n\nAtte.\n\nEquipo '+empresa.nombre,
			empresa.correo,
			[pedido.email],
			fail_silently=False,
		)
		sweetify.success(request, 'Gracias por su compra, si todo está correcto su pedido llegará de 3 a 5 días hábiles, si tiene alguna duda o consulta puede realizarla al whatsapp de servicio '+empresa.telefono+' ó enviar un correo a: '+empresa.correo+', será un placer atenderle', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	else:
		sweetify.error(request, 'Seleccione una imagen por favor', persistent=':(')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def voucher(request, id):
	empresa = Empresa.objects.last()
	total = 0
	pedido = Pedido.objects.get(id=id)
	plan = "Total a pagar"
	precio = pedido.total.amount
	logo = Empresa.objects.last()
	productos = Producto_Pedido.objects.filter(pedido=pedido)
	arreglo = {}
	for x in productos:
		arreglo[x.id] = {"nombre":x.producto.nombre,
			"precio":x.producto.precio.amount,
			"cantidad":x.cantidad,
			"talla":x.talla,
			"total":x.cantidad*x.producto.precio.amount,
			"imagen":x.producto.imagenes.first().imagen.url}
	envio = Envio.objects.last()
	coenvio = envio.costo.amount
	if pedido.ciudad == "Tuxtla Gutiérrez":
		coenvio = 0.00
	arreglo["Envio"] = {"nombre":"envio",
			"precio":coenvio,
			"cantidad":1,
			"talla":"",
			"total":coenvio,
			"imagen":""}
	pdf= render_pdf("pagos.html",{"empresa":empresa,"plan":plan, "precio":precio, "logo":logo.logo.url, "ncuenta":logo.numero_de_cuenta, "cart":arreglo})
	return HttpResponse(pdf,content_type="application/pdf")

def mensajeinfopro(request):
	empresa = Empresa.objects.last()
	producto = Producto.objects.get(id=request.POST.get("productoid"))
	send_mail(
			'Informacion sobre producto '+ producto.nombre +' ' + empresa.nombre ,
			'La persona '+ request.POST.get("nombre") + ' ' + request.POST.get("apellido") + ' con el correo '+request.POST.get("email") + " desea saber informacion sobre el producto:\n" + producto.nombre,
			request.POST.get("email"),
			[empresa.correo],
			fail_silently=False,
		)
	send_mail(
			'Informacion sobre producto '+ producto.nombre +' ' + empresa.nombre ,
			'Tu solicitud de informacion sobre el producto ' + producto.nombre + ' ha sido resibida un asesor se pondrá en contacto contigo',
			empresa.correo,
			[request.POST.get("email")],
			fail_silently=False,
		)
	Mensaje.objects.create(nombre = request.POST.get("nombre"),
		asunto = "Información sobre el producto "+producto.nombre,
		email = request.POST.get("email"),
		telefono= request.POST.get("telefono"),
		mensaje = "El usuario " + request.POST.get("nombre") + " " + request.POST.get("apellido") + " desea saber información sobre el producto: \n" + producto.nombre,
		estado ="Sin leer")
	sweetify.success(request, 'El mensaje ha sido enviado nuestro equipo se pondrá en contacto con usted', persistent=':(')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
