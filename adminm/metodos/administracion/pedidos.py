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
from django.core.mail import EmailMessage, send_mail
import sweetify
import operator
import json
# Pedidos
@csrf_exempt
def showpedidos(request):
	pedidos = Pedido.objects.all().order_by("-id")
	usuarios = User.objects.all()
	pedidos = serializers.serialize('json', pedidos)
	lista = {}
	for usuario in usuarios:
		lista[usuario.id] = usuario.first_name + " " + usuario.last_name
	data = {"pedidos":pedidos, "usuarios":lista}
	return JsonResponse(data, safe=False)

@csrf_exempt
def showmodificarpedidos(request):
	pedido = Pedido.objects.get(id=request.POST.get("id"))
	productos = Producto_Pedido.objects.filter(pedido=pedido)
	listaproductos = {}
	for producto in productos:
		listaproductos[producto.id]={"id":producto.id,
			"imagen":producto.producto.imagenes.first().imagen.url,
			"nombre":producto.producto.nombre,
			"talla":producto.talla,
			"cantidad":producto.cantidad,
			"precio":producto.producto.precio.amount,
			"total":producto.producto.precio.amount*producto.cantidad}
	if pedido.comprobante:
		comprobante = pedido.comprobante.url
	else:
		comprobante = ""
	data = [{"tipo":"label","label":"Pedido"},
			{"tipo":"pedido", "label":"Pedido", "valor":listaproductos},
			{"tipo":"select3","valor":"estadopedido", "sel":pedido.estado_pedido, "label":"Estado del pedido:", "opciones":{'1':'Pago Pendiente','2':'Pagado',"3":'En Camino',"4":'Entregado'}, "name":"estadopedido"},
			{"tipo":"char2","valor":pedido.servicio_mensajeria,"label":"Serivicio de Mensajería:", "name":"servicio_mensajeria"},
			{"tipo":"char2","valor":pedido.numero_guia,"label":"Numero de Guia:", "name":"numero_guia"},
			{"tipo":"modalimagen","valor":comprobante,"label":"Comprobante:", "name":"comprobante"},
			{"tipo":"label","label":" Datos del cliente"},
			{"tipo":"char","valor":pedido.usuario.first_name + " " + pedido.usuario.last_name,"label":"Usuario:", "name":"usuario"},
			{"tipo":"char","valor":pedido.email,"label":"Correo Electrónico:", "name":"email"},
			{"tipo":"char","valor":pedido.telefono,"label":"Telefono:", "name":"telefono"},
			{"tipo":"label","label":" Datos de envio"},
			{"tipo":"char","valor":pedido.direccion,"label":"Dirección:", "name":"direccion"},
			{"tipo":"char","valor":pedido.ciudad,"label":"Ciudad:", "name":"ciudad"},
			{"tipo":"char","valor":pedido.estado,"label":"Estado:", "name":"estado"},
			{"tipo":"char","valor":pedido.pais,"label":"País:", "name":"pais"},
			{"tipo":"char","valor":pedido.codigopostal,"label":"Codigo Postal:", "name":"codigopostal"},]
		
	return JsonResponse(data, safe=False)

@csrf_exempt
def agregarpedido(request):
	listaproductos = request.POST.getlist("productos")
	productos = Producto.objects.filter(id__in=listaproductos)
	pedido = Pedido.objects.create(nombre=request.POST.get("nombre"),
		imagen_representativa=request.FILES["imagen"])
	pedido.productos.add(*productos)
	pedido.save()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def modificarpedido(request):
	empresa = Empresa.objects.last()
	pedido = Pedido.objects.get(id=request.POST.get("idpedido"))
	pedido.estado_pedido = request.POST.get("estadopedido")
	if "comprobante" in request.FILES:
		pedido.comprobante = request.FILES["comprobante"]
	pedido.numero_guia = request.POST.get("numero_guia")
	pedido.servicio_mensajeria = request.POST.get("servicio_mensajeria")
	pedido.save()
	if request.POST.get("estadopedido") == "2" or request.POST.get("estadopedido") == "3" or request.POST.get("estadopedido") == "4":
		if not Venta.objects.filter(usuario=pedido.usuario, monto=pedido.total, pedido=pedido).exists():
			venta = Venta.objects.create(usuario=pedido.usuario, fecha=datetime.now(), monto=pedido.total, pedido=pedido)
			empresa = Empresa.objects.last()
			send_mail(
				'Encuesta de servicio '+empresa.nombre,
				'Gracias por comprar en '+
				empresa.nombre+
				"\n\nHemos preparado una encuesta para evaluar la experiencia que has tenido al comprar con nosotros, nos gustaría conocer tu opinión al respecto y así mejorar nuestros productos y servicios.\n\n"+
				empresa.link_encuesta+
				"\n\nAgradecemos de antemano tu colaboración y la posibilidad de mejorar\n\nHa sido un placer atenderte\n\nTe esperamos pronto\n\nAtentamente\n\nEquipo "+
				empresa.nombre,
				empresa.correo,
				[pedido.email],
				fail_silently=False,
			)
		if request.POST.get("estadopedido") == "2":
			send_mail(
				'Muchas gracias por comprar en '+empresa.nombre+'.',
				'Muchas gracias por comprar en '+
				empresa.nombre+
				"\n\nTu pago fue aprobado y estaremos procesando tu pedido de forma inmediata.\n\n"+
				"Pronto estarás recibiendo un correo con la información de tu envío. "+
				"\n\nHa sido un placer atenderte.\n\nTe esperamos pronto\n\nAtentamente\n\nEquipo "+
				empresa.nombre,
				empresa.correo,
				[pedido.email],
				fail_silently=False,
			)
		if request.POST.get("estadopedido") == "3":
			send_mail(
				'Tu pedido en '+empresa.nombre+' va en camino.',
				'Muchas gracias por comprar en '+
				empresa.nombre+
				"\n\nA continuación se despliega la información sobre el envío de tu pedido.\n\n\nServicio de Mensajería: "+
				pedido.servicio_mensajeria+"\n\nNumero de guia: "+
				pedido.numero_guia+
				"\n\nPuedes rastrearlo directamente en la página web de la mensajería.\n\nSi tienes alguna duda, puedes contactarnos al WhatsApp de servicio "+
				empresa.telefono+
				" y alguien de nuestro equipo te apoyará con todo gusto.\n\nHa sido un placer atenderte.\n\nTe esperamos pronto de regreso.\n\nEquipo "+
				empresa.nombre,
				empresa.correo,
				[pedido.email],
				fail_silently=False,
			)
		if request.POST.get("estadopedido") == "4":
			send_mail(
				'Muchas gracias por comprar en '+empresa.nombre,
				'Muchas gracias por comprar en '+
				empresa.nombre+
				"\n\nSi tienes alguna duda, puedes contactarnos al WhatsApp de servicio "+
				empresa.telefono+
				" y alguien de nuestro equipo te apoyará con todo gusto.\n\nHa sido un placer atenderte.\n\nTe esperamos pronto de regreso.\n\nEquipo "+
				empresa.nombre,
				empresa.correo,
				[pedido.email],
				fail_silently=False,
			)
	if request.POST.get("estadopedido") == "1":
		if Venta.objects.filter(usuario=pedido.usuario, monto=pedido.total, pedido=pedido).exists():
			venta = Venta.objects.get(usuario=pedido.usuario, monto=pedido.total, pedido=pedido)
			venta.delete()
	return JsonResponse("Correcto", safe=False)

@csrf_exempt
def eliminarpedido(request):
	pedido = Pedido.objects.get(id=request.POST.get("id"))
	id = pedido.id
	# Eliminacion de pedidos obsoletos
	if pedido.estado_pedido == "1":
		if not pedido.comprobante:
			pedidoprod = Producto_Pedido.objects.filter(pedido=pedido)
			for producto in pedidoprod:
				if Talla.objects.filter(nombre=producto.talla).exists():
					print("hola")
					talla = Talla.objects.get(nombre=producto.talla)
					if Inventario_Talla.objects.filter(producto=producto.producto, talla=talla).exists():
						inventariotalla = Inventario_Talla.objects.get(producto=producto.producto, talla=talla)
						inventariotalla.cantidad += producto.cantidad
						producto.producto.inventario += producto.cantidad
						inventariotalla.save()
						producto.producto.save()
	pedido.delete()
	return JsonResponse(id, safe=False)