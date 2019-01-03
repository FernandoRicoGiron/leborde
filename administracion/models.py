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
# import conekta
import json
from ckeditor.fields import RichTextField
from django_cleanup.signals import cleanup_pre_delete, cleanup_post_delete
from ecommerce.models import *
from sitio.models import *
from djmoney.models.fields import MoneyField

ESTADO_PEDIDO = (
	('1','PAGO PENDIENTE'),
	('2','PAGADO'),
	("3",'EN CAMINO'),
	("4",'ENTREGADO'),
)

ESTADO_MENSAJE = (
	('Sin leer','Sin leer'),
	('Leido','Leido'),
)

# Pedido
class Pedido(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	total = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	fecha = models.DateTimeField(blank=True, null=True)
	nombre = models.CharField(max_length=100, blank=True, null=True)
	estado_pedido = models.CharField(max_length=100, blank=True, null=True, choices=ESTADO_PEDIDO)
	telefono = models.CharField(max_length=100, blank=True, null=True)
	pais = models.CharField(max_length=100, blank=True, null=True)
	estado = models.CharField(max_length=100, blank=True, null=True)
	ciudad = models.CharField(max_length=100, blank=True, null=True)
	direccion = models.CharField(max_length=200, blank=True, null=True)
	codigopostal = models.CharField(max_length=100, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.usuario.username

# Productos pedido
class Producto_Pedido(models.Model):
	producto = models.ForeignKey("ecommerce.Producto", on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=0)
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
	talla = models.CharField(max_length=100)

	def __str__(self):
		return self.producto.nombre

# Clientes
class Cliente(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	telefono = models.CharField(max_length=100, blank=True, null=True)
	direccion = models.CharField(max_length=100, blank=True, null=True)
	ciudad = models.CharField(max_length=100, blank=True, null=True)
	estado = models.CharField(max_length=100, blank=True, null=True)
	pais = models.CharField(max_length=100, blank=True, null=True)
	codigopostal = models.CharField(max_length=100, blank=True, null=True)
	# id_conekta = models.CharField(max_length=100, blank=True, null=True)
	# id_pago = models.CharField(max_length=100, blank=True, null=True)
	# id_envio = models.CharField(max_length=100, blank=True, null=True)
	token_req = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.usuario.username
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Cliente.objects.create(usuario=instance)

# Contacto
class Mensaje(models.Model):
	nombre = models.CharField(max_length=100)
	asunto = models.CharField(max_length=100)
	email = models.EmailField()
	mensaje = models.TextField()
	estado = models.CharField(choices=ESTADO_MENSAJE, max_length=50)
	
	def __str__(self):
		return self.email

# Ventas
class Venta(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha = models.DateTimeField()
	monto = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

	def __str__(self):
		return self.usuario.username
