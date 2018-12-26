

// Mostrar tabla de mensajes
$("#mostrarMensajes").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Mensajes").attr('href', '#');
	var table = $('#TablaMensajes').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmensajes/', // the file to call
                success: function(json) { // on success..
                	mensajes = JSON.parse(json.mensajes);
 					$.each( mensajes, function( key, value ) {
 						datos = value.fields;
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})

 					if (datos.estado == "Leido") {
						estadopedido = '<i class="material-icons text-success">report</i> <a style="position:absolute" href="#">Leido</a>'
					}
					else if (datos.estado == "Sin leer") {
						estadopedido = '<i class="material-icons text-warning">report</i> <a style="position:absolute" href="#">Sin Leer</a>'
					}
					table.row.add( [value.pk,
						datos.nombre,
						datos.asunto,
						datos.email,
						estadopedido,
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarMensaje btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">search</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarMensaje btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Mensajes").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaMensajes").on('click', 'button.modificarMensaje', function(event) {
	$("#secc").html("Regresar a Mensajes").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarmensaje/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarmensajes/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs2("modificarCampos",json)
                	$("#formmodificar").append('<input type="hidden" name="idmensaje" value="'+id+'"/>')
                	$("#botonModificar").html("Contestar")
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Eliminar Mensajes
$("#TablaMensajes").on('click', 'button.eliminarMensaje', function(event) {
	var table = $('#TablaMensajes').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar este mensaje?',
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
                url: "eliminarmensaje/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu mensaje ha sido eliminado.',
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

