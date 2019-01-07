

// Mostrar tabla de envio
$("#mostrarEnvio").on("click", function () {
	$("#secc").html("Costo de envio").attr('href', '#');
	$(".seccion").hide("fast");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarenvio/');

	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarenvio/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	seccionInputs("modificarCampos",json)
                	
                    
                }
            });
	$(".botonCancelar").hide();
	$("#modificar").show("slow");
});

