

// Mostrar tabla de ventas
$("#mostrarVentas").on("click", function () {
	$(".botonCancelar").show();
	$("#urlventas").val("showventas/")
	url = $("#urlventas").val()
	$(".seccion").hide("fast");
	$("#secc").html("Ventas").attr('href', '#');
	var table = $('#TablaVentas').DataTable();
	table.clear().draw();
        	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: url, // the file to call
                success: function(json) { // on success..
                	ventas = json.ventas;
                	listaventas = json.listaventas
                	$("#myChart").remove();
                	$("#secciondeventas").append('<canvas id="myChart" style="width:100%; max-height:450px;"></canvas>')
                	var ctx = document.getElementById("myChart").getContext('2d');
					var myChart = new Chart(ctx, {
					    type: 'line',
					    data: {
					        labels: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"],
					        datasets: [{
					            label: "Ventas",
					            data: [ventas.lunes, ventas.martes, ventas.miercoles, ventas.jueves, ventas.viernes, ventas.sabado,ventas.domingo],
					            borderColor: [
					                'rgba(67, 160, 71, 1)',
					            ],
					            pointBackgroundColor: 'rgba(67, 160, 71, 1)',
					        }]

					    },
					    options: {
					    	legend: {
					            display: true,
					            labels: {
					                usePointStyle: true,
					            }
					        },
					        scales: {
					            yAxes: [{
					                ticks: {
					                    beginAtZero:true,
					                    callback: function(value, index, values) {
					                        return '$ ' + value;
					                    }
					                }
					            }]
					        }
					    }
					});
                    $("#fechah4").html("Ventas de la semana : "+json.semana);
                    //  Tabla
                    $.each( listaventas, function( key, value ) {

 						var date = new Date(value.fecha);
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
						table.row.add( [value.id,
							(date.getDate()).toString()+"/"+(date.getMonth()+1).toString()+"/"+(date.getFullYear()).toString()+" "+(date.getHours()).toString()+":"+(date.getMinutes()).toString()+":"+(date.getSeconds()).toString(),
							value.nombre,
							"$"+value.total,
                  		] ).node().id = value.pk;
				});
					table.draw();
					$("#ventastabla").html("Ventas : $ "+json.totalventas)

                }

                

            });
    $("#fechainputsend").val(0);
    $("#ventassiguiente").prop('disabled', true);
    $("#Ventas").show("slow");
    $("#agregarCampos").html("");
    $("#modificarCampos").html("");
})

// Mostrar tabla de ventas
$("#ventasanterior").on("click", function () {
	urlac = $("#urlventas").val()
	if (urlac == "showventas/") {
		urlsend = "showventasanterior/"
		etiquetas = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
	}
	else if (urlac == "showventasmensual/") {
		urlsend = "showventasanteriormes/";
		etiquetas = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
	}
	multiplicador = parseInt($("#fechainputsend").val())
	multiplicador = multiplicador+1;
	var table = $('#TablaVentas').DataTable();
	table.clear().draw();
        	$.ajax({ // create an AJAX call...
                data: {multiplicador:multiplicador}, // get the form data
                type: 'POST', // GET or POST
                url: urlsend, // the file to call
                success: function(json) { // on success..
                	ventas = json.ventas;
                	listaventas = json.listaventas
                	if (urlac == "showventas/") {
						datos = [ventas.lunes, ventas.martes, ventas.miercoles, ventas.jueves, ventas.viernes, ventas.sabado,ventas.domingo]
						$("#fechah4").html("Ventas de la semana : "+json.semana);
						
					}
					else if (urlac == "showventasmensual/") {
						datos = [ventas.enero, ventas.febrero, ventas.marzo, ventas.abril, ventas.mayo, ventas.junio,ventas.julio, ventas.agosto, ventas.septiembre, ventas.octubre, ventas.noviembre, ventas.diciembre]
						$("#fechah4").html("Ventas del año : "+json.año);
					}
                	
                	$("#myChart").remove();
                	$("#secciondeventas").append('<canvas id="myChart" style="width:100%; max-height:450px;"></canvas>')
                	var ctx = document.getElementById("myChart").getContext('2d');
					var myChart = new Chart(ctx, {
					    type: 'line',
					    data: {
					        labels: etiquetas,
					        datasets: [{
					            label: "Ventas",
					            data: datos,
					            borderColor: [
					                'rgba(67, 160, 71, 1)',
					            ],
					            pointBackgroundColor: 'rgba(67, 160, 71, 1)',
					        }]

					    },
					    options: {
					    	legend: {
					            display: true,
					            labels: {
					                usePointStyle: true,
					            }
					        },
					        scales: {
					            yAxes: [{
					                ticks: {
					                    beginAtZero:true,
					                    callback: function(value, index, values) {
					                        return '$ ' + value;
					                    }
					                }
					            }]
					        }
					    }
					});

					//  Tabla
                    $.each( listaventas, function( key, value ) {

 						var date = new Date(value.fecha);
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
						table.row.add( [value.id,
							(date.getDate()).toString()+"/"+(date.getMonth()+1).toString()+"/"+(date.getFullYear()).toString()+" "+(date.getHours()).toString()+":"+(date.getMinutes()).toString()+":"+(date.getSeconds()).toString(),
							value.nombre,
							"$"+value.total,
                  		] ).node().id = value.pk;
				});
					table.draw();
					$("#ventastabla").html("Ventas : $ "+json.totalventas)
                }
            });
            $("#fechainputsend").val(multiplicador);
            if (multiplicador != 0) {
            	$("#ventassiguiente").prop('disabled', false);
            }
            else{
            	$("#ventassiguiente").prop('disabled', true);
            }
})

// Mostrar tabla de ventas
$("#ventassiguiente").on("click", function () {
	urlac = $("#urlventas").val()
	if (urlac == "showventas/") {
		urlsend = "showventassiguiente/"
		etiquetas = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
	}
	else if (urlac == "showventasmensual/") {
		urlsend = "showventassiguientemes/";
		etiquetas = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
	}
	multiplicador = parseInt($("#fechainputsend").val())
	multiplicador = multiplicador-1;

	var table = $('#TablaVentas').DataTable();
	table.clear().draw();
        	$.ajax({ // create an AJAX call...
                data: {multiplicador:multiplicador}, // get the form data
                type: 'POST', // GET or POST
                url: urlsend, // the file to call
                success: function(json) { // on success..
                	ventas = json.ventas;
                	listaventas = json.listaventas
                	if (urlac == "showventas/") {
						datos = [ventas.lunes, ventas.martes, ventas.miercoles, ventas.jueves, ventas.viernes, ventas.sabado,ventas.domingo]
						$("#fechah4").html("Ventas de la semana : "+json.semana);
						
					}
					else if (urlac == "showventasmensual/") {
						datos = [ventas.enero, ventas.febrero, ventas.marzo, ventas.abril, ventas.mayo, ventas.junio,ventas.julio, ventas.agosto, ventas.septiembre, ventas.octubre, ventas.noviembre, ventas.diciembre]
						$("#fechah4").html("Ventas del año : "+json.año);
					}
                	
                	$("#myChart").remove();
                	$("#secciondeventas").append('<canvas id="myChart" style="width:100%; max-height:450px;"></canvas>')
                	var ctx = document.getElementById("myChart").getContext('2d');
					var myChart = new Chart(ctx, {
					    type: 'line',
					    data: {
					        labels: etiquetas,
					        datasets: [{
					            label: "Ventas",
					            data: datos,
					            borderColor: [
					                'rgba(67, 160, 71, 1)',
					            ],
					            pointBackgroundColor: 'rgba(67, 160, 71, 1)',
					        }]

					    },
					    options: {
					    	legend: {
					            display: true,
					            labels: {
					                usePointStyle: true,
					            }
					        },
					        scales: {
					            yAxes: [{
					                ticks: {
					                    beginAtZero:true,
					                    callback: function(value, index, values) {
					                        return '$ ' + value;
					                    }
					                }
					            }]
					        }
					    }
					});
                    //  Tabla
                    $.each( listaventas, function( key, value ) {

 						var date = new Date(value.fecha);
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
						table.row.add( [value.id,
							(date.getDate()).toString()+"/"+(date.getMonth()+1).toString()+"/"+(date.getFullYear()).toString()+" "+(date.getHours()).toString()+":"+(date.getMinutes()).toString()+":"+(date.getSeconds()).toString(),
							value.nombre,
							"$"+value.total,
                  		] ).node().id = value.pk;
				});
					table.draw();
					$("#ventastabla").html("Ventas : $ "+json.totalventas)
                }
            });
            $("#fechainputsend").val(multiplicador);
            if (multiplicador != 0) {
            	$("#ventassiguiente").prop('disabled', false);
            }
            else{
            	$("#ventassiguiente").prop('disabled', true);
            }
})


$("#changesemanal").on("click", function () {
	$("#ventassiguiente").html("Semana siguiente");
	$("#ventasanterior").html("Semana anterior");
	$("#mostrarVentas").click();
})

$("#changemensual").on("click", function () {
	$("#ventassiguiente").html("Mes siguiente");
	$("#ventasanterior").html("Mes anterior");
	$("#mostrarVentas").click();
	$("#urlventas").val("showventasmensual/")
	url = $("#urlventas").val()
	var table = $('#TablaVentas').DataTable();
	table.clear().draw();
	$.ajax({ // create an AJAX call...
                data: {}, // get the form data
                type: 'POST', // GET or POST
                url: url, // the file to call
                success: function(json) { // on success..
                	ventas = json.ventas;
                	listaventas = json.listaventas
                	$("#myChart").remove();
                	$("#secciondeventas").append('<canvas id="myChart" style="width:100%; max-height:450px;"></canvas>')
                	var ctx = document.getElementById("myChart").getContext('2d');
					var myChart = new Chart(ctx, {
					    type: 'line',
					    data: {
					        labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
					        datasets: [{
					            label: "Ventas",
					            data: [ventas.enero, ventas.febrero, ventas.marzo, ventas.abril, ventas.mayo, ventas.junio,ventas.julio, ventas.agosto, ventas.septiembre, ventas.octubre, ventas.noviembre, ventas.diciembre],
					            borderColor: [
					                'rgba(67, 160, 71, 1)',
					            ],
					            pointBackgroundColor: 'rgba(67, 160, 71, 1)',
					        }]

					    },
					    options: {
					    	legend: {
					            display: true,
					            labels: {
					                usePointStyle: true,
					            }
					        },
					        scales: {
					            yAxes: [{
					                ticks: {
					                    beginAtZero:true,
					                    callback: function(value, index, values) {
					                        return '$ ' + value;
					                    }
					                }
					            }]
					        }
					    }
					});
                    $("#fechah4").html("Ventas del año : "+json.año);
                    //  Tabla
                    $.each( listaventas, function( key, value ) {

 						var date = new Date(value.fecha);
 						// $.each( datos.imagenes, function( key, value ) {console.log(value)})
						table.row.add( [value.id,
							(date.getDate()).toString()+"/"+(date.getMonth()+1).toString()+"/"+(date.getFullYear()).toString()+" "+(date.getHours()).toString()+":"+(date.getMinutes()).toString()+":"+(date.getSeconds()).toString(),
							value.nombre,
							"$"+value.total,
                  		] ).node().id = value.pk;
				});
					table.draw();
					$("#ventastabla").html("Ventas : $ "+json.totalventas)
                }
            });
    $("#fechainputsend").val(0);
    $("#ventassiguiente").prop('disabled', true);
})

$("#changeanual").on("click", function () {
	$("#mostrarVentas").click();
})