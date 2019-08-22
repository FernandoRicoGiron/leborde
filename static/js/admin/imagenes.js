$("#agregarCampos").on("change", "input#files", function() {
	var formData = new FormData($("#formagregar")[0]);
	$.ajax({ // create an AJAX call...
                data: formData, // get the form data
                type: "POST", // GET or POST
                url: "agregarimagenes/", // the file to call
                contentType: false,
                processData: false,
                success: function(json) { // on success..
                	// console.log(json)
                	$.each(json,function(index, el) {
                		document.getElementById("list").innerHTML += ['<div id="imagen'+el.id+'" class="col-md-3 reagregado" style="height:250px;"><img style="width:100%; position:absolute;" class="thumb" src="', el.url,'"/><a href="javascript:return false" class="eliminarimagen"><i style="position:absolute; background: #f33527; border-radius: 50%;" class="material-icons">clear</i></a><input class="idimagenes" type="hidden" name="idimagenes" value="'+el.id+'"/></div>'].join('');
                	});
                	
                    
                },

                error: function (request, status, error) {
			        swal('¡Oops!',
					  'Algo ha ido mal, verifique bien los datos',
					  'error')
			    },
            });
});

$("#agregarCampos").on("change", "input.files2", function() {
    readURL(this, $(this).attr('name'));
});

$("#modificarCampos").on("change", "input.files2", function() {
    readURL(this, $(this).attr('name'));
});
// $("#modificarCampos").on("change", "input.files3", function() {
//     readURL(this, $(this).attr('name'));
// });

function readURL(input, name) {

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
       document.getElementById("list"+name).innerHTML = ['<div class="col-md-12" style=""><img style="max-width:100%;" class="thumb" src="', e.target.result,'"/></div>'].join('');
      
    }

    reader.readAsDataURL(input.files[0]);
  }
}


$("#agregarCampos").on('click', 'a.eliminarimagen', function() {
	id = $(this).parent().find("input.idimagenes").val();
	$.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: "POST", // GET or POST
                url: "eliminarimagenes/", // the file to call
                success: function(json) { // on success..
                	$("#imagen"+id).remove()
                	
                	
                    
                },

                error: function (request, status, error) {
			        swal('¡Oops!',
					  'Algo ha ido mal, verifique bien los datos',
					  'error')
			    },
            });
});


$("#modificarCampos").on("change", "input#files", function() {
    var formData = new FormData($("#formmodificar")[0]);
    $.ajax({ // create an AJAX call...
                data: formData, // get the form data
                type: "POST", // GET or POST
                url: "agregarimagenes/", // the file to call
                contentType: false,
                processData: false,
                success: function(json) { // on success..
                    // console.log(json)
                    $.each(json,function(index, el) {
                        document.getElementById("list").innerHTML += ['<div id="imagen'+el.id+'" class="col-md-3 reagregado" style="height:250px;"><img style="width:100%; position:absolute;" class="thumb" src="', el.url,'"/><a href="javascript:return false" class="eliminarimagen"><i style="position:absolute; background: #f33527; border-radius: 50%;" class="material-icons">clear</i></a><input class="idimagenes" type="hidden" name="idimagenesnu" value="'+el.id+'"/></div>'].join('');
                    });
                    
                    
                },

                error: function (request, status, error) {
                    swal('¡Oops!',
                      'Algo ha ido mal, verifique bien los datos',
                      'error')
                },
            });
});

$("#modificarCampos").on('click', 'a.eliminarimagen', function() {
    id = $(this).parent().find("input.idimagenes").val();
    
    $("#imagen"+id).remove()
});

$("#secc").on('click', function() {
    $(".reagregado").each(function() {
        
        id = $(this).attr('id').replace("imagen","");
        
        $.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: "POST", // GET or POST
                url: "eliminarimagenes/", // the file to call
                success: function(json) { // on success..
                    $("#imagen"+id).remove()
                    
                    
                    
                },

                error: function (request, status, error) {
                    swal('¡Oops!',
                      'Algo ha ido mal, verifique bien los datos',
                      'error')
                },
            });
    });
    
});

$(".botonCancelar").on('click', function() {
    $(".reagregado").each(function() {
        
        id = $(this).attr('id').replace("imagen","");
        
        $.ajax({ // create an AJAX call...
                data: {id:id}, // get the form data
                type: "POST", // GET or POST
                url: "eliminarimagenes/", // the file to call
                success: function(json) { // on success..
                    $("#imagen"+id).remove()
                    irProductos();
                    
                    
                    
                },

                error: function (request, status, error) {
                    swal('¡Oops!',
                      'Algo ha ido mal, verifique bien los datos',
                      'error')
                },
            });
    });
    
});

