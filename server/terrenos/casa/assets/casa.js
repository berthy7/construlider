main_route = '/casa'

$(document).ready(function () {

});


$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});



function cargar_tabla(data){

    if ( $.fn.DataTable.isDataTable( '#data_table' ) ) {
        var table = $('#data_table').DataTable();
        table.destroy();
    }

    $('#data_table').DataTable({
        data:           data,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,

          columnDefs: [
            {
                targets: 10,
                className: 'text-center'
            },
            {
                targets: 11,
                className: 'text-center'
            }
          ],

        dom: "Bfrtip" ,
        buttons: [
            // {  extend : 'excelHtml5',
            //    exportOptions : { columns : [0, 1, 2, 3, 4, 5 ,6 ,7]},
            //     sheetName: 'Reporte Areas Sociales',
            //    title: 'reas Sociales'  },
            // {  extend : 'pdfHtml5',
            //     orientation: 'landscape',
            //    customize: function(doc) {
            //         doc.styles.tableBodyEven.alignment = 'center';
            //         doc.styles.tableBodyOdd.alignment = 'center';
            //    },
            //    exportOptions : {
            //         columns : [0, 1, 2, 3, 4, 5 ,6 ,7]
            //     },
            //    title: 'reas Sociales'
            // }
        ],
        initComplete: function () {


        },
        "order": [[ 0, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}

$('#fkurbanizacion').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkmanzano').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkurbanizacion').change(function () {

    cargar_manzanos($('#fkurbanizacion').val())
    validationInputSelectsWithReturn("form")

});

function cargar_manzanos(idurbanizacion) {
        obj = JSON.stringify({
        'idurbanizacion': parseInt(idurbanizacion),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "manzano_listar_x_urbanizacion";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)



        $('#fkmanzano').html('');
        var select = document.getElementById("fkmanzano")
        for (var i = 0; i < Object.keys(response.response).length; i++) {

            if (i == 0){
                $('#valorMetroCuadrado').val(response['response'][i]['urbanizacion']['valorMetroCuadrado'])
                $('#fkmoneda').val(response['response'][i]['urbanizacion']['fkmoneda'])
                $('#fkmoneda').selectpicker('refresh')
            }

            var option = document.createElement("OPTION");
            option.innerHTML = "Nro. " + response['response'][i]['numero'] + ": " + response['response'][i]['calle1'] + " - " + response['response'][i]['calle2'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkmanzano').selectpicker('refresh');

    })

}


$('#new').click(function () {
    $('#norte').val('')
    $('#sur').val('')
    $('#este').val('')
    $('#oeste').val('')
    $('#superficie').val('')
    $('#superficieConstruida').val('')
    $('#valorMetroCuadrado').val('')
    $('#fkurbanizacion').val('')
    $('#fkurbanizacion').selectpicker('refresh')
    $('#fkmanzano').val('')
    $('#fkmanzano').selectpicker('refresh')
    $('#fkmoneda').val('')
    $('#fkmoneda').selectpicker('refresh')

    $('#foto1').fileinput('clear');
    $('#foto2').fileinput('clear');
    $('#foto3').fileinput('clear');
    $('#foto4').fileinput('clear');
    $('.nfoto').hide()


    verif_inputs('')
    validationInputSelects("form")

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').on('click',function (e) {
    e.preventDefault();
    objeto_verificar = JSON.stringify({
        'idurbanizacion': $('#fkurbanizacion').val(),
    })
    ajax_call_post("casa_verificar", {
        _xsrf: getCookie("_xsrf"),
        object: objeto_verificar
    }, function (response) {
         if(response.success === true){

             notvalid = validationInputSelectsWithReturn("form");
            if (notvalid===false) {
                var data = new FormData($('#form_submit')[0]);

                objeto = JSON.stringify({
                    'norte': $('#norte').val(),
                    'sur': $('#sur').val(),
                    'este': $('#este').val(),
                    'oeste': $('#oeste').val(),
                    'superficie': $('#superficie').val(),
                    'superficieConstruida': $('#superficieConstruida').val(),
                    'valorMetroCuadrado': $('#valorMetroCuadrado').val(),
                    'fkmoneda': $('#fkmoneda').val(),
                    'fkmanzano': $('#fkmanzano').val()

                })

                data.append('object', objeto)
                data.append('_xsrf', getCookie("_xsrf"))

                render = null
                callback = function () {
                    setTimeout(function () {
                        window.location = main_route
                    }, 2000);
                }

                $.ajax({
                    url: 'casa_insert',
                    type: "post",
                    data: data,
                    contentType: false,
                    processData: false,
                    cache: false,
                    async: false
                }).done(function (response) {
                    if (render != null) {
                        $(render).html(response)
                    } else {
                        dictionary = JSON.parse(response)
                        if ("message" in dictionary && dictionary.message !== '') {
                            if (dictionary.success) showMessage(dictionary.message, "success", "ok")
                            else showMessage(dictionary.message, "danger", "remove")
                        }
                    }
                    if (callback != null)  callback(response)
                })
                $('#form').modal('hide')


            } else {
                swal(
                    'Error de datos.',
                     notvalid,
                    'warning'
                )
            }

         }else{
             swal(
                'Error de datos.',
                 'ya se alcanzo el nro maximo de Casas ',
                'warning'
            )

         }

    })
})


function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('casa_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#norte').val(self.norte)
            $('#sur').val(self.sur)
            $('#este').val(self.este)
            $('#oeste').val(self.oeste)
            $('#superficie').val(self.superficie)
            $('#superficieConstruida').val(self.superficieConstruida)
            $('#valorMetroCuadrado').val(self.valorMetroCuadrado)    
            $('#fkmoneda').val(self.fkmoneda)
            $('#fkmoneda').selectpicker('refresh')
            $('#fkurbanizacion').val(self.manzano.fkurbanizacion)
            $('#fkurbanizacion').selectpicker('refresh')

            cargar_manzanos($('#fkurbanizacion').val())

            $('#fkmanzano').val(self.fkmanzano)
            $('#fkmanzano').selectpicker('refresh')
        
            if (self.foto1 != "None" && self.foto1 != "") {
                document.getElementById("imagen_show_img").src = self.foto1;
            } else {
                document.getElementById("imagen_show_img").src = "/resources/images/sinImagen.jpg";
            }
            if (self.foto2 != "None" && self.foto2 != "") {
                document.getElementById("imagen_show_img2").src = self.foto2;
            } else {
                document.getElementById("imagen_show_img2").src = "/resources/images/sinImagen.jpg";
            }
            if (self.foto3 != "None" && self.foto3 != "") {
                document.getElementById("imagen_show_img3").src = self.foto3;
            } else {
                document.getElementById("imagen_show_img3").src = "/resources/images/sinImagen.jpg";
            }
            if (self.foto4 != "None" && self.foto4 != "") {
                document.getElementById("imagen_show_img4").src = self.foto4;
            } else {
                document.getElementById("imagen_show_img4").src = "/resources/images/sinImagen.jpg";
            }

            $('#foto1').fileinput('clear');
            $('#foto2').fileinput('clear');
            $('#foto3').fileinput('clear');
            $('#foto4').fileinput('clear');
            $('.nfoto').show()
        
            clean_form()
            verif_inputs('')
            validationInputSelects("form")
            $('#id_div').show()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
    })
    }

$('#update').on('click',function (e) {
    e.preventDefault();
    objeto_verificar = JSON.stringify({
        'idurbanizacion': $('#fkurbanizacion').val(),
    })
    ajax_call_post("casa_verificar", {
        _xsrf: getCookie("_xsrf"),
        object: objeto_verificar
    }, function (response) {
         if(response.success === true){

             notvalid = validationInputSelectsWithReturn("form");
            if (notvalid===false) {
                var data = new FormData($('#form_submit')[0]);

                objeto = JSON.stringify({
                    'id': $('#id').val(),
                    'norte': $('#norte').val(),
                    'sur': $('#sur').val(),
                    'este': $('#este').val(),
                    'oeste': $('#oeste').val(),
                    'superficie': $('#superficie').val(),
                    'superficieConstruida': $('#superficieConstruida').val(),
                    'valorMetroCuadrado': $('#valorMetroCuadrado').val(),
                    'fkmoneda': $('#fkmoneda').val(),
                    'fkmanzano': $('#fkmanzano').val()

                })

                data.append('object', objeto)
                data.append('_xsrf', getCookie("_xsrf"))

                render = null
                callback = function () {
                    setTimeout(function () {
                        window.location = main_route
                    }, 2000);
                }

                $.ajax({
                    url: 'casa_update',
                    type: "post",
                    data: data,
                    contentType: false,
                    processData: false,
                    cache: false,
                    async: false
                }).done(function (response) {
                    if (render != null) {
                        $(render).html(response)
                    } else {
                        dictionary = JSON.parse(response)
                        if ("message" in dictionary && dictionary.message !== '') {
                            if (dictionary.success) showMessage(dictionary.message, "success", "ok")
                            else showMessage(dictionary.message, "danger", "remove")
                        }
                    }
                    if (callback != null)  callback(response)
                })
                $('#form').modal('hide')


            } else {
                swal(
                    'Error de datos.',
                     notvalid,
                    'warning'
                )
            }

         }else{
             swal(
                'Error de datos.',
                 'ya se alcanzo el nro maximo de terrenos ',
                'error'
            )

         }

    })
})
reload_form()


function eliminar(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Casa?"

    } else {
        cb_title = "¿Habilitar Casa?"
    }
    swal({
        title: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#393939",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })
        ajax_call('casa_delete', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    })
}



validationKeyup("form")
validationSelectChange("form")

