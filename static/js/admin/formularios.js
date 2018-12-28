// Funcion generadora de inputs
function seccionInputs(campos, json) {
	$.each( json, function( key, value ) {
		tipo = value.tipo;
		valor = value.valor;
		label = value.label;
		name = value.name;
		if (tipo == "char") {
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input name="'+name+'" type="text" class="form-control" value="'+valor+'">'+
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
	                      '<input id="'+name+'" name="'+name+'" type="password" class="form-control" value="">'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "text"){
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
	                      '<div class="form-group">'+
	                        '<label class="bmd-label-floating">'+label+'</label>'+
	                        '<textarea name="'+name+'" class="form-control" rows="5">'+valor+'</textarea>'+
	                      '</div>'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "ckeditor"){
			input = '<div class="col-md-12">'+
	                    '<div class="form-group">'+
	                      '<div class="form-group">'+
	                        '<label class="bmd-label-floating">'+label+'</label>'+
	                        '<textarea name="'+name+'" id="editor'+name+'" rows="10" cols="80">'+valor+'</textarea>'+
	                      '</div>'+
	                    '</div>'+
	                  '</div>';
	        $("#"+campos).append(input)
	        CKEDITOR.replace( 'editor'+name );
		}
		else if(tipo == "money"){
			input = '<div class="col-md-6">'+
	                    '<div class="form-group">'+
	                      '<label class="bmd-label-floating">'+label+'</label>'+
	                      '<input name="'+name+'" type="number" step="0.01" class="form-control" value="'+valor+'">'+
	                    '</div>'+
	                  '</div>';
		}
		else if(tipo == "bolean"){
			if (valor) {
				popular = '<div class="form-check"><label class="form-check-label"><input name="'+name+'" class="form-check-input che" type="checkbox" value="True" checked=""> <span class="form-check-sign"><span class="check"></span></span>'+label+'</label></div>';
			}
			else{
				popular = '<div class="form-check"><label class="form-check-label"><input name="'+name+'" class="form-check-input che" type="checkbox" value="False"> <span class="form-check-sign"><span class="check"></span></span>'+label+'</label></div>';
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
	                      '<input name="'+name+'" type="number" class="form-control" value="'+valor+'">'+
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
		else if (tipo == "imagen"){
			file = '<div class="col-md-12">'+
						'<div class="form-group">'+
						  '<label class="bmd-label-floating">'+label+'</label>'+
			              '<span class="btn btn-info btn-file" ><input style="z-index: 10000;" type="file" id="files" name="'+name+'" multiple accept="image/jpeg, image/png"/><p style="z-index: -10000; margin-bottom:0">Imagenes</p></span></a>'+
			            '</div>'+
			            '<div id="list" class="row" style="height:350px; overflow-y:auto;"></div>'+
		            '</div>';
		    // alert(file)
		    $("#"+campos).append(file)
		    // document.getElementById('files').addEventListener('change', archivo, false);
		    if (valor != "") {
		    	$.each(valor,function(index, el) {
                		document.getElementById("list").innerHTML += ['<div id="imagen'+el.id+'" class="col-md-3" style="height:250px;"><img style="width:100%; position:absolute;" class="thumb" src="', el.url,'"/><a href="javascript:return false" class="eliminarimagen"><i style="position:absolute; background: #f33527; border-radius: 50%;" class="material-icons">clear</i></a><input class="idimagenes" type="hidden" name="idimagenes" value="'+el.id+'"/></div>'].join('');
                	});
		    }
		    

		}
		else if (tipo == "imagen2"){
			file = '<div class="col-md-7">'+
						'<div class="form-group">'+
						  '<label class="bmd-label-floating">'+label+'</label>'+
			              '<span class="btn btn-info btn-file" ><input style="z-index: 10000;" type="file" id="files2" name="'+name+'" accept="image/jpeg, image/png"/><p style="z-index: -10000; margin-bottom:0">Seleccione la imagen que representa a la colección</p></span></a>'+
			            '</div>'+
			            '<div id="list" class="row" style=""></div>'+
		            '</div>';
		    // alert(file)
		    $("#"+campos).append(file)
		    // document.getElementById('files').addEventListener('change', archivo, false);
		    if (valor != "") {
                document.getElementById("list").innerHTML = ['<div class="col-md-9" style=""><img style="max-width:100%" class="thumb" src="', valor,'"/></div>'].join('');
                	
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
	        if (value.sel != "") {
	        	seleccionados = JSON.parse(value.sel);
	        }
	        else{
	        	seleccionados = "";
	        }
		    lista = []
		     $.each( seleccionados, function( key, val ) {
					idse = val.pk;
					lista.push(idse)
					
				});	
	        if (lista.length > 0) {
		       
	        	$('.mdb-select').multiselect('select', lista)
	    	}
		}
		if (tipo != "imagen" & tipo != "imagen2" & tipo != "multiselect" & tipo != "ckeditor") {
			$("#"+campos).append(input)
		}

	});
	
	

}