main_route = '/urbanizacion'

id_gv = 0

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
                targets: 8,
                className: 'text-center'
            },
            {
                targets: 9,
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
        "order": [[ 0, "asc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}

function append_input_manzano(id_in) {
    
        if(id_in === ''){
        id_gv++;
        id_in = id_gv;
    }
    
    
    $('#manzano_div').append(
    '<div class="row">\
        <div class="col-sm-1 hidden">\
            <div class="input-group">\
            <input  id="id'+id_in+'" class="form-control idmanzano manzano readonly txta-own">\
            </div>\
        </div>\
        <div class="col-sm-2">\
            <div class="form-line">\
            <input  id="numero'+id_in+'" value="'+id_in+'" class="form-control manzano txta-own">\
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
    </div>\
    <br>\
    '
    )

    $('.clear_vivienda').last().click(function () {
        $(this).parent().parent().remove()
    })
}

$('#new_manzano').click(function () {
    parent_div = document.getElementById('manzano_div');
    current_cant = $(parent_div).children().length;
    cant_create = document.getElementById('numeroManzanos').value !== ''? parseInt(document.getElementById('numeroManzanos').value): 0;
    dif_cant = cant_create - current_cant;


    if (dif_cant > 0) {
        for (var i = 0; i < dif_cant; i++) {

            append_input_manzano('')
        }
    } else if (dif_cant < 0) {
        for (var j = current_cant; j > cant_create; j--) {
            $( "#manzano_div div.row").last().remove()
            
            id_gv = id_gv - 1
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


        objeto.push((function add_(h0, h1, h2, h3) {
            if (h0 === ''){
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
        })( h0, h1, h2, h3))
    }

    return objeto
}

$('#new').click(function () {
    id_gv = 0
    $('#nombre').val('')
    $('#direccion').val('')
    $('#uv').val('')
    $('#valorMetroCuadrado').val('')
    $('#fkmoneda').val(2)
    $('#fkmoneda').selectpicker('refresh')
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

    if (parseInt($('#numeroManzanos').val()) !=  parseInt($('.idmanzano').length)){
        swal(
            'Error de datos.',
             'el numero de manzanos maximo, no coincide con el numero de manzanos creados',
            'warning'
        )
    }else{
        notvalid = validationInputSelectsWithReturn("form");

        if (notvalid === false) {
            objeto = JSON.stringify({
                'nombre': $('#nombre').val(),
                'direccion': $('#direccion').val(),
                'uv': $('#uv').val(),
                'valorMetroCuadrado': $('#valorMetroCuadrado').val(),
                'numeroTerrenos': $('#numeroTerrenos').val(),
                'fkmoneda': $('#fkmoneda').val(),
                'manzanos': get_manzano(),
                'numeroCasas': $('#numeroCasas').val(),
                'numeroManzanos': $('#numeroManzanos').val()
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
            $('#nombre').val(self.nombre)
            $('#direccion').val(self.direccion)
            $('#uv').val(self.uv)
            $('#valorMetroCuadrado').val(self.valorMetroCuadrado)
            $('#fkmoneda').val(self.fkmoneda)
            $('#fkmoneda').selectpicker('refresh')
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
            $('#id_div').show()
            $('#insert').hide()
            $('#update').show()
            $('#form').modal('show')
    })
}

$('#update').click(function () {

    if (parseInt($('#numeroManzanos').val()) !=  parseInt($('.idmanzano').length)){

        swal(
            'Error de datos.',
             'el numero de manzanos maximo, no coincide con el numero de manzanos creados',
            'warning'
        )
    }else{

        notvalid = validationInputSelectsWithReturn("form");

        if (notvalid === false) {
            objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'nombre': $('#nombre').val(),
                'direccion': $('#direccion').val(),
                'uv': $('#uv').val(),
                'valorMetroCuadrado': $('#valorMetroCuadrado').val(),
                'fkmoneda': $('#fkmoneda').val(),
                'numeroTerrenos': $('#numeroTerrenos').val(),
                'numeroCasas': $('#numeroCasas').val(),
                'numeroManzanos': $('#numeroManzanos').val(),
                'manzanos': get_manzano()
            })
            data = JSON.parse(objeto)
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
