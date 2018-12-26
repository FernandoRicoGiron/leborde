

// Mostrar tabla de datos
$("#mostrarDE").on("click", function () {
	$("#secc").html("Datos de la empresa").attr('href', '#');
	$(".seccion").hide("fast");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificardato/');

	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificardatos/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	seccionInputs("modificarCampos",json)
                	
                    
                }
            });
	$(".botonCancelar").hide();
	$("#modificar").show("slow");
});

