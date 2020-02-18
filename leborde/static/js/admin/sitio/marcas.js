

// Mostrar tabla de marcas
$("#mostrarMarcas").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Marcas").attr('href', '#');
	var table = $('#TablaMarcas').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmarcas/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	marcas = JSON.parse(json);
 					$.each( marcas, function( key, value ) {
 						datos = value.fields;
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
					table.row.add( ['<center><image class="center-items mdl-grid" style="width:80px;" src="/media/'+datos.imagen+'"></center>',
						value.pk,
						datos.nombre,
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarMarca btn btn-success" data-original-title="" title="">'+
	                      '<i class="material-icons">edit</i>'+
	                    '</button>'+
	                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarMarca btn btn-danger" data-original-title="" title="">'+
	                      '<i class="material-icons">close</i>'+
	                    '</button>',
                  ] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Marcas").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaMarcas").on('click', 'button.modificarMarca', function(event) {
	$("#secc").html("Regresar a Marcas").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarmarca/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarmarcas/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idmarca" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Agregar
$("#agregarMarca").on('click', function(event) {
	$("#secc").html("Regresar a Marcas").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarmarca/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarmarcas/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});




// Eliminar Marcas
$("#TablaMarcas").on('click', 'button.eliminarMarca', function(event) {
	var table = $('#TablaMarcas').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar este marca?',
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
                url: "eliminarmarca/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu marca ha sido eliminado.',
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

