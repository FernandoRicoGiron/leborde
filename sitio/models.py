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
from administracion.models import *

# Sitio
class Carrusel(models.Model):
	texto = models.CharField(max_length=100, blank=True)
	imagen = models.ImageField(upload_to="Carrusel")
	url = models.URLField(blank=True)

	class Meta:
		verbose_name = "Carrusel"
		verbose_name_plural = "Carruseles"

	def __str__(self):
		return "Carrusel" + " " +str(self.id)

class Marca(models.Model):
	nombre = models.CharField(max_length=100)
	imagen = models.ImageField(upload_to="Marcas", blank=True, null=True)

	def __str__(self):
		return self.nombre

class FAQ(models.Model):
	pregunta = models.CharField(max_length=200)
	respuesta = RichTextField()

	def __str__(self):
		return self.pregunta

class Secciones(models.Model):
	tituloqs = models.CharField(max_length=200, default="¿Quiénes Somos?")
	imagenqs = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	titulot = models.CharField(max_length=200, default="Tienda")
	imagent = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	tituloc = models.CharField(max_length=200, default="Contacto")
	imagenc = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	titulodp = models.CharField(max_length=200, default="Datos para el pago")
	imagendp = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	tituloppaypal = models.CharField(max_length=200, default="Proceder al pago con paypal")
	imagenppaypal = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	titulop = models.CharField(max_length=200, default="Datos de perfil")
	imagenp = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	titulopedidos = models.CharField(max_length=200, default="Mis Pedidos")
	imagenpedidos = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")
	titulopreguntas = models.CharField(max_length=200, default="Preguntas Frecuentes")
	imagenpreguntas = models.ImageField(upload_to="Secciones", blank=True, null=True, default="coleccion3.jpg")

	def __str__(self):
		return "Secciones del sitio"

class Empresa(models.Model):
	nombre = models.CharField(max_length=100)
	logo = models.ImageField(upload_to="Logo")
	direccion = models.CharField(max_length=100)
	telefono = models.CharField(max_length=100)
	correo = models.CharField(max_length=100)
	correopaypal = models.CharField(max_length=100)
	titulo = models.CharField(blank=True, null=True, max_length=50)
	giro_de_la_empresa = models.TextField(blank=True, null=True)
	numero_de_cuenta = models.CharField(max_length=50)
	link_encuesta = models.URLField(blank=True, null=True)
	facebook = models.URLField(blank=True, null=True)
	twiter = models.URLField(blank=True, null=True)
	instagram = models.URLField(blank=True, null=True)
	youtube = models.URLField(blank=True, null=True)

	def __str__(self):
		return self.nombre

class QuienesSomos(models.Model):
	titulo = models.CharField(max_length=100)
	texto = RichTextField(blank=True, null=True)

	def __str__(self):
		return self.titulo
