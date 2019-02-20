

// Mostrar tabla de pedidos
$("#mostrarPedidos").on("click", function () {
	$(".botonCancelar").show();
	$(".seccion").hide("fast");
	$("#secc").html("Pedidos").attr('href', '#');
	var table = $('#TablaPedidos').DataTable();
        	table.clear();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showpedidos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	pedidos = JSON.parse(json.pedidos);
                	clientes = json.usuarios;
 					$.each( pedidos, function( key, value ) {
 						
 						datos = value.fields;
 						// alert(datos.comprobante)
 						if (datos.comprobante != "" & datos.estado_pedido != 2 & datos.estado_pedido != 3 & datos.estado_pedido != 4) {
 							estadopedido = '<i class="material-icons text-warning">report</i> <a style="position:absolute" href="#">Con comprobante</a>'
 						}
 						else if (datos.estado_pedido == 1) {
 							estadopedido = '<i class="material-icons text-danger">report</i> <a style="position:absolute" href="#">Pago Pendiente</a>'
 						}
 						else if (datos.estado_pedido == 2) {
 							estadopedido = '<i class="material-icons text-warning">report</i> <a style="position:absolute" href="#">Pagado</a>'
 						}
 						else if (datos.estado_pedido == 3) {
 							estadopedido = '<i class="material-icons text-warning">report</i> <a style="position:absolute" href="#">En Camino</a>'
 						}
 						else if (datos.estado_pedido == 4) {
 							estadopedido = '<i class="material-icons text-success">report</i> <a style="position:absolute" href="#">Entregado</a>'
 						}

 						var date = new Date(datos.fecha);
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
						table.row.add( [value.pk,
							(date.getDate()).toString()+"/"+(date.getMonth()+1).toString()+"/"+(date.getFullYear()).toString()+" "+(date.getHours()).toString()+":"+(date.getMinutes()).toString()+":"+(date.getSeconds()).toString(),
							clientes[datos.usuario],
							estadopedido,
							"$"+datos.total,
		                    '<button style="padding:10px;" type="button" rel="tooltip" class="modificarPedido btn btn-success" data-original-title="" title="">'+
		                      '<i class="material-icons">search</i>'+
		                    '</button>'+
		                    '<button style="padding:10px;" type="button" rel="tooltip" class="eliminarPedido btn btn-danger" data-original-title="" title="">'+
		                      '<i class="material-icons">close</i>'+
		                    '</button>',
                  		] ).node().id = value.pk;
				});
					table.draw();
                    
                }
            });
    $("#Pedidos").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})



// Modificar

$("#TablaPedidos").on('click', 'button.modificarPedido', function(event) {
	$("#secc").html("Regresar a Pedidos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	id = $(this).parent().parent().attr("id");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarpedido/');

	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarpedidos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs2("modificarCampos",json)
                	$("#modificarCampos").append('<input type="hidden" name="idpedido" value="'+id+'"/>')
                	
                    
                }
            });

	$("#modificar").show("slow");
});

// Agregar
$("#agregarPedido").on('click', function(event) {
	$("#secc").html("Regresar a Pedidos").attr('href', 'javascript:irAtras()');
	$(".seccion").hide("fast");
	$("#agregarCampos").html("")
	$("#formagregar").attr('action', 'agregarpedido/')
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showagregarpedidos/', // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	seccionInputs("agregarCampos",json)

                	
                    
                },
            });

	$("#agregar").show("slow");
});




// Eliminar Pedidos
$("#TablaPedidos").on('click', 'button.eliminarPedido', function(event) {
	var table = $('#TablaPedidos').DataTable();
	boton = $(this);
 
	id = $(this).parent().parent().attr("id");
	swal({
		  title: '¿Estas seguro que deseas eliminar este pedido?',
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
                url: "eliminarpedido/", // the file to call
                success: function(json) { // on success..
                	// console.log(json)
                	swal(
				      '¡Eliminado!',
				      'Tu pedido ha sido eliminado.',
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

