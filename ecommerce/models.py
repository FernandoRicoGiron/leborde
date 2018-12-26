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

class Sub_Categoria(models.Model):
	nombre = models.CharField(max_length=100)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField()
	precio = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	precio_oferta = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
	popular = models.BooleanField(default=False)
	imagenes = models.ManyToManyField(Imagen)
	inventario = models.IntegerField()
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre

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

