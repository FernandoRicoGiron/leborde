

// Mostrar tabla de colecciones
$("#mostrarColecciones").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Colecciones").attr('href', '#');
	var table = $('#TablaColecciones').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showcolecciones/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	colecciones = JSON.parse(json);
 					$.each( colecciones, function( key, value ) {
 						datos = value.fields;
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
					table.row.add( ["<center><image class='center-items mdl-grid' style='width:80px;' src='/media/"+datos.imagen_representativa+"' /></center>",
						value.pk,
						datos.nombre,
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarColeccion btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">edit</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarColeccion btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Colecciones").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaColecciones").on('click', 'button.modificarColeccion', function(event) {
	$("#secc").html("Regresar a Colecciones").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarcoleccion/');
	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarcolecciones/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idcoleccion" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Agregar
$("#agregarColeccion").on('click', function(event) {
	$("#secc").html("Regresar a Colecciones").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarcoleccion/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarcolecciones/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});




// Eliminar Colecciones
$("#TablaColecciones").on('click', 'button.eliminarColeccion', function(event) {
	var table = $('#TablaColecciones').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar esta coleccion?',
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
                url: "eliminarcoleccion/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu coleccion ha sido eliminado.',
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

