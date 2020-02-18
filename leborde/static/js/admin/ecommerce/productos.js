// Mostrar Productos
$("#mostrarPricipal").on("click", function () {
	$(".botonCancelar").show();
	$("#secc").html("Principal").attr('href', '#');
	$(".seccion").hide("fast");
	$("#Principal").show("slow");
});

// Mostrar tabla de productos
$("#mostrarProductos").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Productos").attr('href', '#');
	var table = $('#TablaProductos').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showproductos/', // the file to call
                success: function(json) { // on success..
                	productos = JSON.parse(json.productos);
                	imagenes = json.imagenes
                	categorias = json.categorias
 					$.each( productos, function( key, value ) {
 						datos = value.fields;
 						console.log(value)
 						if (datos.popular) {
 							popular = '<i class="material-icons text-success">done</i> <a style="position:absolute" href="#">Popular</a>'
 						}
 						else  {
 							popular = '<i class="material-icons text-danger">clear</i> <a style="position:absolute" href="#">No popular</a>'
 						}
 						
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
					table.row.add( ['<center><image class="center-items mdl-grid" style="width:80px;" src="'+imagenes[datos.imagenes[0]]+'"></center>',
						value.pk,
						datos.nombre,
						"$ "+datos.precio,
						datos.inventario,
						popular,
						categorias[datos.categoria],
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarProducto btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">edit</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarProducto btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Productos").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaProductos").on('click', 'button.modificarProducto', function(event) {
	$("#secc").html("Regresar a Productos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarproducto/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarproductos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idproducto" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Funcion Modificar
$("#botonModificar").on('click', function() {
	/* Act on the event */
	if ($("#formmodificar").attr('action') == "modificardato/" | $("#formmodificar").attr('action') == "modificarpregunta/" | $("#formmodificar").attr('action') == "modificarquienessomos/"| $("#formmodificar").attr('action') == "modificardato/") {
		for ( instance in CKEDITOR.instances )
    		CKEDITOR.instances[instance].updateElement();
	}
	var formData = new FormData($("#formmodificar")[0]);
	if($('#contraseña').length){
		var password = document.getElementById("contraseña");
    	var confirm = document.getElementById("recontraseña");
	}
	else{
		var password = "null";
    	var confirm = "null";
	}
	if((password.value == confirm.value & password != "null" & confirm != "null") | $("#formmodificar").attr('action') != "modificarcliente/"){
	$.ajax({ // create an AJAX call...
                data: formData, // get the form data
                type: $("#formmodificar").attr('method'), // GET or POST
                url: $("#formmodificar").attr('action'), // the file to call
                contentType: false,
                processData: false,
                success: function(json) { // on success..
                	// console.log(json)
                	if (json == "Correcto") {
	                	swal('¡Genial!',
						  '¡Todo ha ido correctamente!',
						  'success')
	                	irAtras()
	                }
	                else{
	                	swal('Oops!',
						  json,
						  'error')
	                }
                	
                    
                },

                error: function (request, status, error) {
			        swal('¡Oops!',
					  'Algo ha ido mal, verifique bien los datos',
					  'error')
			    },
            });
		}
	else{
            swal({
                  type: 'error',
                  title: '¡Oops!',
                  text: '¡Las contraseñas no coinciden!',
                })
            return false;
          } 

});

// Agregar
$("#agregarProducto").on('click', function(event) {
	$("#secc").html("Regresar a Productos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarproducto/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarproductos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});


// Funcion agregar Productos
$("#botonAgregar").on('click', function() {
	/* Act on the event */
	if ($("#formagregar").attr('action') == "agregardato/" | $("#formagregar").attr('action') == "agregarpregunta/" | $("#formagregar").attr('action') == "agregarquienessomos/" | $("#formagregar").attr('action') == "modificardato/") {
		for ( instance in CKEDITOR.instances )
    		CKEDITOR.instances[instance].updateElement();
	}
	var formData = new FormData($("#formagregar")[0]);
	if($('#contraseña').length){
		var password = document.getElementById("contraseña");
    	var confirm = document.getElementById("recontraseña");
	}
	else{
		var password = "null";
    	var confirm = "null";
	}
	
	  if ((password.value == confirm.value & password != "null" & confirm != "null") | $("#formagregar").attr('action') != "agregarcliente/") {
	    $.ajax({ // create an AJAX call...
	        data: formData, // get the form data
	        type: $("#formagregar").attr('method'), // GET or POST
	        url: $("#formagregar").attr('action'), // the file to call
	        contentType: false,
	        processData: false,
	        success: function(json) { // on success..
	        	// console.log(json)
	        	if (json == "Correcto") {
	            	swal('¡Genial!',
					  '¡Todo ha ido correctamente!',
					  'success')
	            	irAtras()
	            }
	            else{
	            	swal('¡Oops!',
					  json,
					  'error')
	            }
	        	
	            
	        },

	        error: function (request, status, error) {
		        swal('¡Oops!',
				  'Algo ha ido mal, verifique bien los datos',
				  'error')
		    },
	    });
	  }
          else{
            swal({
                  type: 'error',
                  title: '¡Oops!',
                  text: '¡Las contraseñas no coinciden!',
                })
            return false;
          } 

	
});

// Ir productos
function irAtras(argument) {
	if ($("#formagregar").attr('action') == "agregarproducto/" | $("#formmodificar").attr('action') == "modificarproducto/") {
		$("#mostrarProductos").click();
	}
	else if($("#formagregar").attr('action') == "agregarcategoria/" | $("#formmodificar").attr('action') == "modificarcategoria/"){
		$("#mostrarCategorias").click();
	}	
	else if($("#formagregar").attr('action') == "agregartalla/" | $("#formmodificar").attr('action') == "modificartalla/"){
		$("#mostrarTallas").click();
	}
	else if($("#formagregar").attr('action') == "agregarcoleccion/" | $("#formmodificar").attr('action') == "modificarcoleccion/"){
		$("#mostrarColecciones").click();
	}
	else if($("#formagregar").attr('action') == "agregarcliente/" | $("#formmodificar").attr('action') == "modificarcliente/"){
		$("#mostrarClientes").click();
	}	
	else if($("#formagregar").attr('action') == "agregarpedido/" | $("#formmodificar").attr('action') == "modificarpedido/"){
		$("#mostrarPedidos").click();
	}
	else if($("#formagregar").attr('action') == "agregarmensaje/" | $("#formmodificar").attr('action') == "modificarmensaje/"){
		$("#mostrarMensajes").click();
	}
	else if($("#formagregar").attr('action') == "agregarcarrusel/" | $("#formmodificar").attr('action') == "modificarcarrusel/"){
		$("#mostrarCarruseles").click();
	}
	else if($("#formagregar").attr('action') == "agregarpregunta/" | $("#formmodificar").attr('action') == "modificarpregunta/"){
		$("#mostrarPreguntas").click();
	}	
	else if($("#formagregar").attr('action') == "agregarmarca/" | $("#formmodificar").attr('action') == "modificarmarca/"){
		$("#mostrarMarcas").click();
	}	
	else if($("#formagregar").attr('action') == "agregarpregunta/" | $("#formmodificar").attr('action') == "modificarpregunta/"){
		$("#mostrarPreguntas").click();
	}	
	else if($("#formagregar").attr('action') == "agregarquienessomos/" | $("#formmodificar").attr('action') == "modificarquienessomos/"){
		$("#mostrarSEQS").click();
	}			
	$("#botonModificar").html("Modificar")
	$(".botonCancelar").show();
}



//Checkbox

$("#agregarCampos").on('change', 'input.che', function() {
	if ($(this).is(':checked')) {
		$(this).val("True")
	}
	else{
		$(this).val("False")
	}
	
});

$("#modificarCampos").on('change', 'input.che', function() {
	if ($(this).is(':checked')) {
		$(this).val("True")
	}
	else{
		$(this).val("False")
	}
	
});




// Eliminar Productos
$("#TablaProductos").on('click', 'button.eliminarProducto', function(event) {
	var table = $('#TablaProductos').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar este producto?',
		  text: "¡No podras recuperarlo!",
		  type: 'warning',
		  showCancelButton: true,
		  confirmButtonColor: '#3085d6',
		  cancelButtonColor: '#d33',
		  confirmButtonText: 'Si, Eliminar',
		  cancelButtonText: 'Cancelar'
		}).then((result) => {
		  if (result.value) {
		  	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: "POST", // GET or POST
                url: "eliminarproducto/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu producto ha sido eliminado.',
				      'success'
				    )
                	table
						        .row( boton.parents('tr') )
						        .remove()
						        .draw();
                    
                },

                error: function (request, status, error) {
			        swal('¡Oops!',
					  'Algo ha ido mal, verifique bien los datos',
					  'error')
			    },
            });
		    
		  }
		})
	
});

$(".botonCancelar").on('click', function() {
	irAtras()
});

