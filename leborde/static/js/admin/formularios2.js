// Funcion generadora de inputs
function seccionInputs2(campos, json) {
	$.each( json, function( key, value ) {
		tipo = value.tipo;
		valor = value.valor;
		label = value.label;
		name = value.name;
		if (tipo == "char") {
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input disabled name="'+name+'" type="text" class="form-control" value="'+valor+'">'+
	                    '</div>'+
	                  '</div>';
		}
		else if (tipo == "label") {
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                    '</div>'+
	                  '</div>';
		}
		else if (tipo == "pass") {
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input disabled id="'+name+'" name="'+name+'" type="password" class="form-control" value="">'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "text"){
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
	                      '<div class="form-group">'+
	                        '<label class="bmd-label-floating">'+label+'</label>'+
	                        '<textarea disabled name="'+name+'" class="form-control" rows="5">'+valor+'</textarea>'+
	                      '</div>'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "text2"){
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
	                      '<div class="form-group">'+
	                        '<label class="bmd-label-floating">'+label+'</label>'+
	                        '<textarea name="'+name+'" class="form-control" rows="5">'+valor+'</textarea>'+
	                      '</div>'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "money"){
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input disabled name="'+name+'" type="number" step="0.01" class="form-control" value="'+valor+'">'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "bolean"){
			if (valor) {
				popular = '<div class="form-check"><label class="form-check-label"><input disabled name="'+name+'" class="form-check-input che" type="checkbox" value="True" checked=""> <span class="form-check-sign"><span class="check"></span></span>'+label+'</label></div>';
			}
			else{
				popular = '<div class="form-check"><label class="form-check-label"><input disabled name="'+name+'" class="form-check-input che" type="checkbox" value="False"> <span class="form-check-sign"><span class="check"></span></span>'+label+'</label></div>';
			}
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      popular+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "int"){
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input disabled name="'+name+'" type="number" class="form-control" value="'+valor+'">'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "select"){
			opciones = JSON.parse(value.opciones);
			opt = "";
			$.each( opciones, function( key, val ) {
				datos = val.fields;
				if (val.pk == value.sel) {
					opt += '<option value="'+val.pk+'" selected>'+datos.nombre+'</option>';
				}
				else{
					opt += '<option value="'+val.pk+'">'+datos.nombre+'</option>';
				}
			});
			

			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<select name="'+name+'" class="form-control">'+
	                      	opt+
	                      '</select>'
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "select3"){
			opciones = value.opciones;
			opt = "";
			$.each( opciones, function( key, val ) {
				if (key == value.sel) {
					opt += '<option value="'+key+'" selected>'+val+'</option>';
				}
				else{
					opt += '<option value="'+key+'">'+val+'</option>';
				}
			});
			

			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<select name="'+name+'" class="form-control">'+
	                      	opt+
	                      '</select>'
	                    '</div>'+
	                  '</div>';
		}
		else if (tipo == "imagen"){
			file = '<div class="col-md-12">'+
						'<div class="form-group">'+
						  '<label class="bmd-label-floating">'+label+'</label>'+
			              '<span class="btn btn-info btn-file" ><input disabled style="z-index: 10000;" type="file" id="files" name="'+name+'" multiple accept="image/jpeg, image/png"/><p style="z-index: -10000; margin-bottom:0">Imagenes</p></span></a>'+
			            '</div>'+
			            '<div id="list" class="row" style="height:350px; overflow-y:auto;"></div>'+
		            '</div>';
		    // alert(file)
		    $("#"+campos).append(file)
		    // document.getElementById('files').addEventListener('change', archivo, false);
		    if (valor != "") {
		    	$.each(valor,function(index, el) {
                		document.getElementById("list").innerHTML += ['<div id="imagen'+el.id+'" class="col-md-3" style="height:250px;"><img style="width:100%; position:absolute;" class="thumb" src="', el.url,'"/><a href="javascript:return false" class="eliminarimagen"><i style="position:absolute; background: #f33527; border-radius: 50%;" class="material-icons">clear</i></a><input disabled class="idimagenes" type="hidden" name="idimagenes" value="'+el.id+'"/></div>'].join('');
                	});
		    }
		    

		}
		else if (tipo == "imagen2"){
			file = '<div class="col-md-12">'+
						'<div class="form-group">'+
						  '<label class="bmd-label-floating">'+label+'</label>'+
			              '<span class="btn btn-info btn-file" ><input style="z-index: 10000;" type="file" id="files2" name="'+name+'" accept="image/jpeg, image/png"/><p style="z-index: -10000; margin-bottom:0">Seleccione una imagen</p></span></a>'+
			            '</div>'+
			            '<div id="list" style="max-width:400px;" class="row" style=""></div>'+
		            '</div>';
		    // alert(file)
		    $("#"+campos).append(file)
		    // document.getElementById('files').addEventListener('change', archivo, false);
		    if (valor != "") {
                document.getElementById("list").innerHTML = ['<div class="col-md-12" style=""><img style="max-width:100%" class="thumb" src="', valor,'"/></div>'].join('');
                	
		    }
		    

		}
		else if(tipo == "multiselect"){
			opciones = JSON.parse(value.opciones);
			opt = "";
			$.each( opciones, function( key, val ) {
				datos = val.fields;
				opt += '<option value="'+val.pk+'">'+datos.nombre+'</option>';
				
			});
			

			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<select searchable="Buscar Aquí.." multiple name="'+name+'" class="form-control mdb-select">'+
	                      	opt+
	                      '</select>'
	                    '</div>'+
	                  '</div>';
	        $("#"+campos).append(input);
	        $('.mdb-select').multiselect({
	        	enableFiltering: true,
	            includeSelectAllOption: true,
	            buttonWidth: '100%',
	        });
	        
	        
	        $("button.multiselect").removeClass( "btn-default" )
	        $("button.multiselect").addClass( "btn-info" )
	        $("button.multiselect-clear-filter").removeClass('btn-default')
	        $("button.multiselect-clear-filter").addClass( "btn-danger" )
	        $("i.glyphicon-remove-circle").attr('class', 'material-icons').html("close");
	        seleccionados = JSON.parse(value.sel);
		    lista = []
		     $.each( seleccionados, function( key, val ) {
					idse = val.pk;
					lista.push(idse)
					
				});	
	        if (lista.length > 0) {
		       
	        	$('.mdb-select').multiselect('select', lista)
	    	}
		}

		else if (tipo == "pedido") {
			pedidos = valor;
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
					'<table class="table row-border" id="tpedidos">'+
                      '<thead class=" text-primary">'+                        
                        '<th>Imagen</th>'+                      
                        '<th>Nombre</th>'+
                        '<th>Talla</th>'+
                        '<th>Cantidad</th>'+
                        '<th>Precio</th>'+
                        '<th>Total</th>'+
                      '</thead>'+
                      '<tbody>'+                        
                      '</tbody>'+
                    '</table>'+
                    '</div></div>';
            $("#"+campos).append(input)
            var tablepedidos = $('#tpedidos').DataTable({
		          language: {
		              "decimal": "",
		              "emptyTable": "No hay información",
		              "info": "Mostrando _START_ a _END_ de _TOTAL_ Productos",
		              "infoEmpty": "Mostrando 0 a 0 de 0 Productos",
		              "infoFiltered": "(Filtrado de _MAX_ total entradas)",
		              "infoPostFix": "",
		              "thousands": ",",
		              "lengthMenu": "Mostrar _MENU_",
		              "loadingRecords": "Cargando...",
		              "processing": "Procesando...",
		              "search": "",
		              "zeroRecords": "Sin resultados encontrados",
		              "paginate": {
		                  "first": "Primero",
		                  "last": "Ultimo",
		                  "next": "Siguiente",
		                  "previous": "Anterior"
		              }

		          },
		          // fixedHeader: true,
		          // "scrollY": 450,
		          // "scrollX": true,
		      });

            $.each( pedidos, function( key, val ) {
					datos=val;
					tablepedidos.row.add( ['<center><image class="center-items mdl-grid" style="width:80px;" src="'+datos.imagen+'"></center>',
						datos.nombre,
						datos.talla,
						datos.cantidad,
						"$ "+datos.precio,
						"$ "+datos.total,
                  ] ).node().id = datos.id;
					
					
				});
			tablepedidos.draw();
			$('div.dataTables_filter input').addClass('form-control form-control-sm');
	        $('div.dataTables_filter input').attr('placeholder','Buscar')
	        $('div.dataTables_length select').addClass('custom-select custom-select-sm form-control form-control-sm');
	        $('div.dataTables_paginate a').addClass('btn btn-primary');
	        $('div.dataTables_filter label').addClass('col-form-label');

		}

		if (tipo != "imagen" & tipo != "imagen2" & tipo != "multiselect" & tipo != "pedido") {
			$("#"+campos).append(input)
		}

	});
	
	

}