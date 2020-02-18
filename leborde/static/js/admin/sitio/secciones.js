

// Mostrar tabla de seccions
$("#mostrarSEC").on("click", function () {
	$("#secc").html("Secciones del sitio").attr('href', '#');
	$(".seccion").hide("fast");
	$("#modificarCampos").html("");
	$("#formmodificar").attr('action', 'modificarseccion/');

	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: 'showmodificarsecciones/', // the file to call
                success: function(json) { // on success..
                	console.log(json)
                	seccionInputs("modificarCampos",json)
                	
                    
                }
            });
	$(".botonCancelar").hide();
	$("#modificar").show("slow");
});

