

// Mostrar tabla de carruseles
$("#mostrarCarruseles").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Carruseles").attr('href', '#');
	var table = $('#TablaCarruseles').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showcarruseles/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	carruseles = JSON.parse(json);
 					$.each( carruseles, function( key, value ) {
 						datos = value.fields;
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
					table.row.add( ['<center><image class="center-items mdl-grid" style="width:80px;" src="/media/'+datos.imagen+'"></center>',
						value.pk,
						datos.texto,
						datos.url,
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarCarrusel btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">edit</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarCarrusel btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Carruseles").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaCarruseles").on('click', 'button.modificarCarrusel', function(event) {
	$("#secc").html("Regresar a Carruseles").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarcarrusel/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarcarruseles/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idcarrusel" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Agregar
$("#agregarCarrusel").on('click', function(event) {
	$("#secc").html("Regresar a Carruseles").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarcarrusel/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarcarruseles/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});




// Eliminar Carruseles
$("#TablaCarruseles").on('click', 'button.eliminarCarrusel', function(event) {
	var table = $('#TablaCarruseles').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar este carrusel?',
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
                url: "eliminarcarrusel/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu carrusel ha sido eliminado.',
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

