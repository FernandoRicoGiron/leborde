

// Mostrar tabla de datos
$("#mostrarContraseña").on("click", function () {
	$("#secc").html("Contraseña").attr('href', '#');
	$(".seccion").hide("fast");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarcontraseña/');

	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarcontraseña/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	seccionInputs("modificarCampos",json)
                	
                    
                }
            });
	$(".botonCancelar").hide();
	$("#modificar").show("slow");
});

