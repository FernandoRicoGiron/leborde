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

class Empresa(models.Model):
	nombre = models.CharField(max_length=100)
	logo = models.ImageField(upload_to="Logo")
	direccion = models.CharField(max_length=100)
	telefono = models.CharField(max_length=100)
	correo = models.CharField(max_length=100)
	mision = RichTextField()
	vision = RichTextField()
	valores = RichTextField()
	historia = RichTextField()
	giro_de_la_empresa = RichTextField()

	def __str__(self):
		return self.nombre
