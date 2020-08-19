main_route = '/contrato'

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
        "order": [[ 0, "asc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}

function append_input_manzano(id_in) {

    $('#manzano_div').append(
    '<div class="row">\
        <div class="col-sm-1 hidden">\
            <div class="input-group">\
            <input  id="id'+id_in+'" class="form-control idmanzano manzano readonly txta-own">\
            </div>\
        </div>\
        <div class="col-sm-2">\
            <div class="form-line">\
            <input  id="numero'+id_in+'" class="form-control manzano txta-own">\
            </div>\
        </div>\
        <div class="col-sm-5">\
            <div class="form-line">\
                <input id="calle1'+id_in+'" data-id="'+id_in+'" class="form-control manzano  txta-own">\
            </div>\
        </div>\
        <div class="col-sm-5">\
            <div  class="form-line">\
                <input id="calle2'+id_in+'" data-id="'+id_in+'" class="form-control manzano  txta-own">\
            </div>\
        </div>\
    </div>'
)

    $('.clear_vivienda').last().click(function () {
        $(this).parent().parent().remove()
    })


}

$('#new_manzano').click(function () {


    console.log("numero de manzanos: "+parseInt($('#numeroManzanos').val()))
    console.log("numero manzanos creados: "+$('.idmanzano').length)

    if(parseInt($('#numeroManzanos').val()) != parseInt($('.idmanzano').length)){

        var cant = parseInt($('#numeroManzanos').val()) - parseInt($('.idmanzano').length)
        console.log(cant)
        if (cant > 0){
            console.log("mayor a cero")
            for (var i = 0; i < parseInt(cant); i++) {

               append_input_manzano('')
            }

        }else{
            console.log("menor a cero")

        }





    }





})

function get_manzano() {
    objeto = []
    objeto_inputs = $('.manzano')

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value


        objeto.push((function add_(h0, h1, h2,h3) {

            if (h0 ==''){
                return {
                    'numero': h1,
                    'calle1': h2,
                    'calle2': h3

                }

            }else{
                return {
                'id':h0,
                'numero': h1,
                'calle1': h2,
                'calle2': h3
                }
            }


        })(
            h0,
            h1,
            h2,
            h3))
    }


    return objeto
}


$('#new').click(function () {
    $('#direccion').val('')
    $('#numeroTerrenos').val('')
    $('#numeroCasas').val('')
    $('#numeroManzanos').val('')
    $('#manzano_div').empty()


    verif_inputs('')
    validationInputSelects("form")

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})


$('#insert').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'direccion': $('#direccion').val(),
            'numeroTerrenos': $('#numeroTerrenos').val(),
            'numeroCasas': $('#numeroCasas').val(),
            'numeroManzanos': $('#numeroManzanos').val(),
            'manzanos': get_manzano()
         
        })
        ajax_call('urbanizacion_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal(
            'Error de datos.',
             notvalid,
            'error'
        )
    }
})


function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('urbanizacion_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#direccion').val(self.direccion)
            $('#numeroTerrenos').val(self.numeroTerrenos)
            $('#numeroCasas').val(self.numeroCasas)
            $('#numeroManzanos').val(self.numeroManzanos)
            $('#manzano_div').empty()

            for (manza in self.manzanos) {

                append_input_manzano(self.manzanos[manza]['id'])
                $('#id' + self.manzanos[manza]['id']).val(self.manzanos[manza]['id'])
                $('#numero' + self.manzanos[manza]['id']).val(self.manzanos[manza]['numero'])
                $('#calle1' + self.manzanos[manza]['id']).val(self.manzanos[manza]['calle1'])
                $('#calle2' + self.manzanos[manza]['id']).val(self.manzanos[manza]['calle2'])
            }


            clean_form()
            verif_inputs('')
            validationInputSelects("form")
            $('#id_div').hide()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
    })
    }

$('#update').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'direccion': $('#direccion').val(),
            'numeroTerrenos': $('#numeroTerrenos').val(),
            'numeroCasas': $('#numeroCasas').val(),
            'numeroManzanos': $('#numeroManzanos').val()
            
        })
        ajax_call('urbanizacion_update', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function () {
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        })
        $('#form').modal('hide')
    } else {
        swal(
            'Error de datos.',
             notvalid,
            'error'
        )
    }
})
reload_form()


function eliminar(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Urbanizacion?"

    } else {
        cb_title = "¿Habilitar Urbanizacion?"
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
        ajax_call('urbanizacion_delete', {
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

