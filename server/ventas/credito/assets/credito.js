main_route = '/credito'

$(document).ready(function () {});

$(document).ajaxStart(function () {});

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
                targets: 6,
                className: 'text-center'
            },
            {
                targets: 7,
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
        "order": [[ 2, "asc" ]],
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

function append_input_cuota(id_in,monto) {
    if(id_in === ''){
        id_gv++;
        id_in = id_gv;
    }

    $('#cuota_div').append(
    '<div class="row clearfix">\
        <div class="col-sm-1 hidden">\
            <div class="input-group">\
            <input  id="id'+id_in+'" class="form-control idcuota cuota readonly txta-own">\
            </div>\
        </div>\
        <div class="col-sm-2">\
            <div class="form-line">\
            <input  id="numero'+id_in+'" value="'+id_in+'" class="form-control cuota txta-own">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div class="form-line">\
                <input id="monto'+id_in+'" value="'+monto+'" class="form-control cuota  txta-own">\
            </div>\
        </div>\
        <div class="col-sm-4">\
            <div  class="form-line">\
                <input id="fecha'+id_in+'" data-id="'+id_in+'" class="form-control cuota  txta-own date_java">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div class="form-line">\
            <input  id="estado'+id_in+'" data-id="'+id_in+'" class="form-control cuota txta-own">\
            </div>\
        </div>\
    </div>'
)

    $('.clear_vivienda').last().click(function () {
        $(this).parent().parent().remove()
    })



    $('.date_java').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        clearButton: false,
        weekStart: 1,
        locale: 'es',
        time: false
    }).on('change', function (e, date) {
        $(this).parent().addClass('focused');
        eraseError(this)
    });

}

$('#new_cuotas').click(function () {
    parent_div = document.getElementById('cuota_div');
    current_cant = $(parent_div).children().length;
    cant_create = document.getElementById('numeroCuotas').value !== ''? parseInt(document.getElementById('numeroCuotas').value): 0;
    dif_cant = cant_create - current_cant;

    obj = JSON.stringify({
        'valorCredito': parseInt($('#label_valor_credito').text()),
        'numeroCuotas': parseInt($('#numeroCuotas').val()),
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_get('contrato_valor_cuota', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        
        var self = response;
        // $('#id_reserva').val(self.id)

        console.log(id_gv)

        for (var i = 0; i <= id_gv; i++) {

            $('#monto' + i).val(self.valorCuota)

        }




        if (dif_cant > 0) {
            for (var i = 0; i < dif_cant; i++) {

                append_input_cuota('',self.valorCuota)

            }
        } else if (dif_cant < 0) {
            for (var j = current_cant; j > cant_create; j--) {
                $( "#cuota_div div.row").last().remove()

                id_gv = id_gv - 1
            }
        }


    })



})

function get_cuota() {
    objeto = []
    objeto_inputs = $('.cuota')

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value


        objeto.push((function add_(h0, h1, h2,h3) {

            if (h0 ==''){
                return {
                    'numero': h1,
                    'monto': h2,
                    'fechaVencimiento': h3

                }

            }else{
                return {
                'id':h0,
                'numero': h1,
                'monto': h2,
                'fechaVencimiento': h3
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
    $('#ancho').val('')
    $('#largo').val('')
    $('#superficie').val('')
    $('#fkurbanizacion').val('')
    $('#fkurbanizacion').selectpicker('refresh')
    $('#fkmanzano').val('')
    $('#fkmanzano').selectpicker('refresh')

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
            'ancho': $('#ancho').val(),
            'largo': $('#largo').val(),
            'superficie': $('#superficie').val(),
            'fkmanzano': $('#fkmanzano').val()
        })
        ajax_call('credito_insert', {
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
    console.log('🚀 ~ editar ~ elemento', elemento);
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('credito_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#fkestadocredito').val(self.fkestadocredito)
            $('#fkestadocredito').selectpicker('refresh')

            $('#fkentidad').val(self.fkentidad)
            $('#fkentidad').selectpicker('refresh')
            $('#capital').val(self.capital)
            $('#numeroCuotas').val(self.numeroCuotas)
            console.log(self)
            $('#cuota_div').empty()

            for (i in self.cuotas) {
                console.log(i)

                append_input_cuota(self.cuotas[i]['id'],self.cuotas[i]['monto'])
                $('#id' + self.cuotas[i]['id']).val(self.cuotas[i]['id'])
                $('#numero' + self.cuotas[i]['id']).val(self.cuotas[i]['numero'])
                $('#monto' + self.cuotas[i]['id']).val(self.cuotas[i]['monto'])
                $('#fecha' + self.cuotas[i]['id']).val(self.cuotas[i]['fechaVencimiento'])
                $('#estado' + self.cuotas[i]['id']).val(self.cuotas[i]['estadocuota']['nombre'])
                
                switch (self.cuotas[i]['estadocuota']['nombre']) {
                  case 'Pagada':
                    $('#estado' + self.cuotas[i]['id']).addClass('color_cuota_pagada');
                      $('#estado' + self.cuotas[i]['id']).addClass('white-own');
                    break;
                  case 'Mora':
                    $('#estado' + self.cuotas[i]['id']).addClass('color_cuota_mora');
                      $('#estado' + self.cuotas[i]['id']).addClass('white-own');
                    break;
                  default:
                }

                


            }

            clean_form()
            verif_inputs('')
            validationInputSelects("form")
            $('#id_div').show()
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
            'ancho': $('#ancho').val(),
            'largo': $('#largo').val(),
            'superficie': $('#superficie').val(),
            'fkmanzano': $('#fkmanzano').val()
            
        })
        ajax_call('credito_update', {
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
        cb_title = "¿Deshabilitar Credito?"

    } else {
        cb_title = "¿Habilitar Credito?"
    }
    swal({
        title: cb_title,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#424A5A",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        objeto = JSON.stringify({
            id: parseInt($(cb_delete).attr('data-id')),
            enabled: $(cb_delete).is(':checked')
        })
        ajax_call('credito_delete', {
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

