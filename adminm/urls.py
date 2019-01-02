from django.urls import path
from django.conf.urls import include
from . import views as vi
from .metodos.ecommerce import *
from .metodos.administracion import *
from .metodos.sitio import *
from .metodos.perfil import *

urlpatterns = [
    path('', vi.index),
    path('admin_session/', vi.admin_session),
    path('iniciardashboard/', vi.iniciardashboard),
    # Productos
    path('showproductos/', productos.showproductos),
    path('showmodificarproductos/', productos.showmodificarproductos),
    path('showagregarproductos/', productos.showagregarproductos),
    path('eliminarproducto/', productos.eliminarproducto),
    path('modificarproducto/', productos.modificarproducto),
    path('agregarproducto/', productos.agregarproducto),
    # Imagenes
    path('agregarimagenes/', imagenes.agregarimagenes),
    path('eliminarimagenes/', imagenes.eliminarimagenes),
    # Categorias
    path('showcategorias/', categorias.showcategorias),
    path('showmodificarcategorias/', categorias.showmodificarcategorias),
    path('showagregarcategorias/', categorias.showagregarcategorias),
    path('eliminarcategoria/', categorias.eliminarcategoria),
    path('modificarcategoria/', categorias.modificarcategoria),
    path('agregarcategoria/', categorias.agregarcategoria),
    # Colecciones
    path('showcolecciones/', colecciones.showcolecciones),
    path('showmodificarcolecciones/', colecciones.showmodificarcolecciones),
    path('showagregarcolecciones/', colecciones.showagregarcolecciones),
    path('eliminarcoleccion/', colecciones.eliminarcoleccion),
    path('modificarcoleccion/', colecciones.modificarcoleccion),
    path('agregarcoleccion/', colecciones.agregarcoleccion),
    # Tallas
    path('showtallas/', tallas.showtallas),
    path('showmodificartallas/', tallas.showmodificartallas),
    path('showagregartallas/', tallas.showagregartallas),
    path('eliminartalla/', tallas.eliminartalla),
    path('modificartalla/', tallas.modificartalla),
    path('agregartalla/', tallas.agregartalla),
    # Clientes
    path('showclientes/', clientes.showclientes),
    path('showmodificarclientes/', clientes.showmodificarclientes),
    path('showagregarclientes/', clientes.showagregarclientes),
    path('eliminarcliente/', clientes.eliminarcliente),
    path('modificarcliente/', clientes.modificarcliente),
    path('agregarcliente/', clientes.agregarcliente),
    # Pedidos
    path('showpedidos/', pedidos.showpedidos),
    path('showmodificarpedidos/', pedidos.showmodificarpedidos),
    # path('showagregarpedidos/', pedidos.showagregarpedidos),
    path('eliminarpedido/', pedidos.eliminarpedido),
    path('modificarpedido/', pedidos.modificarpedido),
    path('agregarpedido/', pedidos.agregarpedido),
    # Ventas
    path('showventas/', ventas.showventas),
    path('showventasanterior/', ventas.showventasanterior),
    path('showventassiguiente/', ventas.showventassiguiente),
    path('showventasmensual/', ventas.showventasmensual),
    path('showventasanteriormes/', ventas.showventasanteriormes),
    path('showventassiguientemes/', ventas.showventassiguientemes),
    # Mensajes
    path('showmensajes/', mensajes.showmensajes),
    path('showmodificarmensajes/', mensajes.showmodificarmensajes),
    path('eliminarmensaje/', mensajes.eliminarmensaje),
    path('modificarmensaje/', mensajes.contestarmensaje),
    # Datos de la empresa
    path('showmodificardatos/', datosempresa.showmodificardatos),
    path('modificardato/', datosempresa.modificardato),
    # Datos de la envio
    path('showmodificarenvio/', costoenvio.showmodificarenvio),
    path('modificarenvio/', costoenvio.modificarenvio),
    # Carruseles
    path('showcarruseles/', carruseles.showcarruseles),
    path('showmodificarcarruseles/', carruseles.showmodificarcarruseles),
    path('showagregarcarruseles/', carruseles.showagregarcarruseles),
    path('eliminarcarrusel/', carruseles.eliminarcarrusel),
    path('modificarcarrusel/', carruseles.modificarcarrusel),
    path('agregarcarrusel/', carruseles.agregarcarrusel),
    # Preguntas
    path('showpreguntas/', preguntas.showpreguntas),
    path('showmodificarpreguntas/', preguntas.showmodificarpreguntas),
    path('showagregarpreguntas/', preguntas.showagregarpreguntas),
    path('eliminarpregunta/', preguntas.eliminarpregunta),
    path('modificarpregunta/', preguntas.modificarpregunta),
    path('agregarpregunta/', preguntas.agregarpregunta),
    # Marcas
    path('showmarcas/', marcas.showmarcas),
    path('showmodificarmarcas/', marcas.showmodificarmarcas),
    path('showagregarmarcas/', marcas.showagregarmarcas),
    path('eliminarmarca/', marcas.eliminarmarca),
    path('modificarmarca/', marcas.modificarmarca),
    path('agregarmarca/', marcas.agregarmarca),
    # Datos perfil
    path('showmodificarperfil/', perfil.showmodificarperfil),
    path('modificarperfil/', perfil.modificarperfil),
    path('logout/', perfil.cerrarsesion),
    # Contraseña
    path('showmodificarcontraseña/', contraseña.showmodificarcontraseña),
    path('modificarcontraseña/', contraseña.modificarcontraseña),
]
