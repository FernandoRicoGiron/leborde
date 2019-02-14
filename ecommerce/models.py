#!/usr/bin/python
# -*- coding: utf-8    -*-
from __future__ import unicode_literals
import os, sys
from django.db import models
from django.utils import timezone
import datetime
from django.db import migrations
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import conekta
import json
from ckeditor.fields import RichTextField
from django_cleanup.signals import cleanup_pre_delete, cleanup_post_delete
from administracion.models import *
from sitio.models import *
from djmoney.models.fields import MoneyField

# Productos
class Imagen(models.Model):
	imagen = models.ImageField(upload_to="Imagenes")

	class Meta:
		verbose_name = "Imagen"
		verbose_name_plural = "Imagenes"

	def __str__(self):
		return (self.imagen.name).replace("Imagenes/","")

class Categoria(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre

class Talla(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	precio = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	precio_oferta = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	popular = models.BooleanField(default=False)
	en_tienda = models.BooleanField(default=True)
	imagenes = models.ManyToManyField(Imagen)
	inventario = models.IntegerField(default=0)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	tallas = models.ManyToManyField(Talla, blank=True)

	def __str__(self):
		return self.nombre

class Inventario_Talla(models.Model):
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=0)

	def __str__(self):
		return self.producto.nombre

class Ficha_Tecnica(models.Model):
	dato = models.CharField(max_length=50)
	valor = models.CharField(max_length=50)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Ficha Tecnica"
		verbose_name_plural = "Fichas Tecnicas"

	def __str__(self):
		return self.nombre


class Coleccion(models.Model):
	nombre = models.CharField(max_length=100)
	imagen_representativa = models.ImageField(upload_to="Colecciones")
	productos = models.ManyToManyField(Producto)

	class Meta:
		verbose_name = "Colección"
		verbose_name_plural = "Colecciones"

	def __str__(self):
		return self.nombre

class Envio(models.Model):
	costo = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')

	def __str__(self):
		return str(self.costo)

class Num_Pedido(models.Model):
	pedido = models.IntegerField(default=1)

	def __str__(self):
		return str(self.pedido)

# Conekta
# Conekta

# class Sale(models.Model):
# 		def __init__(self, *args, **kwargs):
# 			super(Sale, self).__init__(*args, **kwargs)

# 			conekta.api_key = settings.CONEKTA_PRIVATE_KEY

# 		def charge(self, request, user):
# 			try:
# 				customer = conekta.Customer.create({
# 					"name":request.POST.get("nombre"),
# 					"email":request.POST.get("email"),
# 					# "phone": "+529611002890",
# 					# "payment_sources": [{
# 					# 		"token_id": token_id,
# 					# 		"type": "card"
# 					# }],
# 					# "shipping_contacts": [{
# 					# 	"phone": "+529611002890",
# 					# 	"receiver": "Fernando",
# 					# 	"address": {
# 					# 		"street1": "Jardines del Grijalva",
# 					# 		"country": "MX",
# 					# 		"postal_code": "29165"
# 					# 	}
# 					# }]
# 			})
# 				datos = Cliente.objects.get(usuario=user)
# 				datos.id_conekta = customer.id
# 				datos.save()

				
# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						print(y[1])
# 						break		
# 					break
# 				#El pago no pudo ser procesado

# 		def update(self, token_id, request):
# 			try:				
# 				datos = Cliente.objects.get(usuario=request.user)
# 				customer = conekta.Customer.find(datos.id_conekta)
				
# 				if datos.id_pago:
# 					customer.payment_sources[0].delete()
# 				source = customer.createPaymentSource({
# 						"token_id": token_id,
# 						"type": "card"
# 				})
				
# 				datos.id_pago = source.id
# 				datos.save()

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break

# 		def updateenvio(self, request):
# 			try:				
# 				datos = Cliente.objects.get(usuario=request.user)
# 				customer = conekta.Customer.find(datos.id_conekta)
				
# 				if datos.id_envio:
# 					customer.shipping_contacts[0].delete()

# 				source = customer.createShippingContact({
# 					"phone": datos.numtel,
# 					"receiver": request.user.first_name + " " + request.user.last_name,
# 					"address": {
# 						"street1": datos.direccion,
# 						"country": "MX",
# 						"postal_code": datos.codigopostal
# 					}
# 				})
# 				customer.update({
# 					"name":request.user.username,
# 					"email":request.user.email,
# 					"phone": datos.numtel,
				  
# 				})
# 				return source.id

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break

# 		def order(self, token_id, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
								
# 							},
# 					"line_items": productos,
# 					"shipping_contact":{
# 							"phone" : datos.numtel,
# 							"receiver": request.user.first_name + " " + request.user.last_name,
# 							"address": {
# 									"street1": datos.direccion,
# 									"state": datos.estado,
# 									"country": "MX",
# 									"postal_code": datos.codigopostal,
# 									"metadata":{ "soft_validations": True}
# 							}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges": [{
# 						"payment_method":{
# 							"type": "card",
# 							"token_id": token_id
# 						},
# 						"amount": total+envio,
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				return "Correcto"

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break
						
# 		def order2(self, price_in_cents, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
								
# 							},
# 					"line_items": productos,
# 					"customer_info": {
# 						"customer_id": datos.id_conekta
# 					  },

# 					 "shipping_contact":{
# 						"phone" : datos.numtel,
# 						"receiver": request.user.first_name + " " + request.user.last_name,
# 						"address": {
# 								"street1": datos.direccion,
# 								"city":datos.ciudad,
# 								"state": datos.estado,
# 								"country": "MX",
# 								"postal_code": datos.codigopostal,
# 								"metadata":{ "soft_validations": True}
# 						}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges": [{
# 						"payment_method":{
# 							"type": "default",
# 						},
# 						"amount": total+envio,
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				return "Correcto"

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break

# 		def order3(self, price_in_cents, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
# 							},
# 					"line_items": productos,

# 					"shipping_contact":{
# 						"phone" : request.POST.get("telefono"),
# 						"receiver": request.POST.get("nombrerev"),
# 						"address": {
# 								"street1": request.POST.get("direccion"),
# 								"city":request.POST.get("ciudad"),
# 								"state": request.POST.get("estado"),
# 								"country": "MX",
# 								"postal_code": request.POST.get("codigo"),
# 								"metadata":{ "soft_validations": True}
# 						}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges": [{
# 						"payment_method":{
# 							"type": "default",
# 						},
# 						"amount": total+envio,
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				return "Correcto"

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break	

# 		def order4(self, token_id, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
# 							},
# 					"line_items": productos,

# 					"shipping_contact":{
# 						"phone" : request.POST.get("telefono"),
# 						"receiver": request.POST.get("nombrerev"),
# 						"email": request.POST.get("email"),
# 						"address": {
# 								"street1": request.POST.get("direccion"),
# 								"city":request.POST.get("ciudad"),
# 								"state": request.POST.get("estado"),
# 								"country": "MX",
# 								"postal_code": request.POST.get("codigo"),
# 								"metadata":{ "soft_validations": True}
# 						}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges": [{
# 						"payment_method":{
# 							"type": "card",
# 							"token_id": token_id
# 						},
# 						"amount": total+envio,
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				return "Correcto"

# 			except conekta.ConektaError as e:
# 				# print(e)
# 				# return "error"
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break	

# 		def oxxo(self, price_in_cents, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
								
# 							},
# 					"line_items": productos,
# 					"customer_info": {
# 						"customer_id": datos.id_conekta
# 					  },

# 					 "shipping_contact":{
# 						"phone" : datos.numtel,
# 						"receiver": request.user.first_name + " " + request.user.last_name,
# 						"address": {
# 								"street1": datos.direccion,
# 								"city":datos.ciudad,
# 								"state": datos.estado,
# 								"country": "MX",
# 								"postal_code": datos.codigopostal,
# 								"metadata":{ "soft_validations": True}
# 						}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges":[{
# 					  "payment_method": {
# 						"type": "oxxo_cash"
# 					  }
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				order = conekta.Order.find(order.id)
# 				return order

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break

# 		def oxxo2(self, price_in_cents, cart, request):
# 			productos = []
# 			envio = Costo_Envio.objects.first()
# 			envio = int(str("%.2f" % envio.costo).replace(".",""))
# 			meta = {}
# 			total = 0
# 			nombre = ""
# 			a = 1
# 			for item in cart:
# 				meta[str(a)+ " " +item.product.Nombre] = item.descripcion
# 				total_prod = str(item.total_price/item.quantity).replace(".", "")
# 				total += int(total_prod)*item.quantity
# 				productos.append({"name": item.product.Nombre,
# 					"unit_price": total_prod,
# 					"quantity": item.quantity,
# 					"category": item.product.Tipo,
# 					})
# 				a += 1
# 			datos = Cliente.objects.get(usuario=request.user)


# 			try:
# 				order = conekta.Order.create({
# 					"customer_info":{
# 								"customer_id": datos.id_conekta,
# 							},
# 					"line_items": productos,

# 					"shipping_contact":{
# 						"phone" : request.POST.get("telefono"),
# 						"receiver": request.POST.get("nombrerev"),
# 						"address": {
# 								"street1": request.POST.get("direccion"),
# 								"city":request.POST.get("ciudad"),
# 								"state": request.POST.get("estado"),
# 								"country": "MX",
# 								"postal_code": request.POST.get("codigo"),
# 								"metadata":{ "soft_validations": True}
# 						}
# 					},
# 					"shipping_lines":[
# 								{
# 									"amount": envio,
# 									"carrier": "ESTAFETA",
# 								}],
					
# 					"charges":[{
# 					  "payment_method": {
# 						"type": "oxxo_cash"
# 					  }
# 					}],
# 					"currency" : "mxn",
# 					"metadata" : meta
# 					})
# 				order = conekta.Order.find(order.id)
# 				return order

# 			except conekta.ConektaError as e:
# 				for key,value in e.error_json.items():
# 					for y in value[0].items():
# 						return y[1]
# 						break		
# 					break		
# 						# print(str(key)+" "+str(value))
						
# 						#el pago no pudo ser procesado

# 				#You can also get the attributes from the conekta response class:
# 				# print(order.id)

# 				#Or in the event of an error, you can expect a ConektaError to be raised