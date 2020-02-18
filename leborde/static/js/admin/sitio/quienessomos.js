

// Mostrar tabla de quienessomos
$("#mostrarSEQS").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Quiénes Somos").attr('href', '#');
	var table = $('#TablaQuienesSomos').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showquienessomos/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	quienessomos = JSON.parse(json);
 					$.each( quienessomos, function( key, value ) {
 						datos = value.fields;
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
					table.row.add( [value.pk,
						datos.titulo,
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarQuienesSomos btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">edit</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarQuienesSomos btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#QuienesSomos").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaQuienesSomos").on('click', 'button.modificarQuienesSomos', function(event) {
	$("#secc").html("Regresar a Quiénes Somos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarquienessomos/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarquienessomos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idquienessomos" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Agregar
$("#agregarQuienesSomos").on('click', function(event) {
	$("#secc").html("Regresar a QuienesSomos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarquienessomos/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarquienessomos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});




// Eliminar QuienesSomos
$("#TablaQuienesSomos").on('click', 'button.eliminarQuienesSomos', function(event) {
	var table = $('#TablaQuienesSomos').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar esta sección?',
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
                url: "eliminarquienessomos/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu seccion ha sido eliminada.',
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

