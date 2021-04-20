main_route = '/contrato'
id_reserva = null;
id_gv = 0

$(document).ready(function () {

});

$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

$('.date').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    eraseError(this)
});

$('#fkreserva').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione Reserva'
})

$('#fktipoventa').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione venta'
})

$('#fkentidad').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione Entidad'
})

$('#fkreserva').change(function () {

    cargar_detalle_reserva($('#fkreserva').val())

});

$('#fktipoventa').change(function () {

    cargar_tipoventa(parseInt($('#fktipoventa').val()))



});

function cargar_tipoventa(idtipoventa) {

    if(idtipoventa == 1){
        $('#fkentidad').val(idtipoventa)
        $('#fkentidad').selectpicker('refresh')

        $('#numeroCuotas').val(idtipoventa)

        cargar_cuotas()




    }else{
        $('#fkentidad').val('')
        $('#fkentidad').selectpicker('refresh')

        $('#numeroCuotas').val('')
        $('#cuota_div').empty()

    }

}

function cargar_detalle_reserva(idreserva) {

    obj = JSON.stringify({
        'id': parseInt(idreserva),
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_get('contrato_obtener_reserva', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#fkmoneda').val(self.fkmoneda)
            $('#fechaReserva').val(self.fechaReserva)
            $('#label_cliente').html(self.cliente.fullname)
            $('#label_urbanizacion').html(self.terreno.manzano.urbanizacion.nombre)
            $('#label_manzano').html(self.terreno.manzano.numero)
            $('#label_tipo_terreno').html(self.terreno.tipoterreno.nombre)
            $('#label_fecha_reserva').html(self.fechaReserva)
            $('#label_estado_reserva').html(self.estadoreserva.nombre)
            $('#label_monto').html(self.monto)
            $('#label_valor_metro2').html(self.terreno.valorMetroCuadrado)
            $('#label_superficie').html(self.terreno.superficie)
            $('#label_valor_terreno').html(self.valorTerreno)
            $('#label_tasa_interes').html(self.tasaInteres + " %")
            $('#label_interes').html(self.interes)
            $('#label_valor_credito').html(self.valorCredito)
            $('.moneda').html(self.moneda.codigo)

    })

}

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
        "order": [[ 0, "asc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}

function append_input_cuota(id_in) {
    // debugger
    $('#cuota_div').append(
        '<div class="row">\
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
            <div class="col-sm-5">\
                <div class="form-line">\
                    <input id="monto'+id_in+'" value="" class="form-control cuota  txta-own">\
                </div>\
            </div>\
            <div class="col-sm-5">\
                <div  class="form-line">\
                    <input id="fecha'+id_in+'" data-id="'+id_in+'" class="form-control cuota  txta-own date_java">\
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
    if($('#fkreserva').val()){
            if($('#numeroCuotas').val()){
                cargar_cuotas()
            }else{
                swal(
                    'Ingrese nro de cuotas.',
                     ' ',
                    'warning'
                )
            }
    }else{
        swal(
            'Seleccione Reserva.',
             ' ',
            'warning'
        )
    }
})

function cargar_cuotas() {
    // div para rellenar con las cuotas
    // debugger
    parent_div = document.getElementById('cuota_div');
    // cantidad actual o cantidad inicial cuando se muestra el form por primera vez
    current_cant = $(parent_div).children().length;
    console.log('🚀 ~ cargar_cuotas ~ current_cant', current_cant);
    // Si el numero de cuotas introducido es distinto de cero
    cant_create = document.getElementById('numeroCuotas').value !== '' ? parseInt(document.getElementById('numeroCuotas').value): 0;
    // 
    dif_cant = cant_create - current_cant;

    if( $('#fechaPrimerCuota').val()== ""){
        var fechahoy = new Date();
        var hoy = "28/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()
        document.getElementById("fechaPrimerCuota").value=hoy
    }

    obj = JSON.stringify({
        'valorCredito': parseInt($('#label_valor_credito').text()),
        'numeroCuotas': parseInt($('#numeroCuotas').val()),
        'cuotaInicial': parseInt($('#cuotaInicial').val()),
        'montoReserva': parseInt($('#label_monto').text()),
        'fechaPrimerCuota': $('#fechaPrimerCuota').val(),
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_get('contrato_valor_cuota', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

        // Vacia el div para rellenar luego
        $('#cuota_div').empty()
        
        for (i in self) {
            append_input_cuota(self[i].numero)
            $('#numero' + self[i].numero).val(self[i].numero)
            $('#monto' + self[i].numero).val(self[i].valorCuota)
            $('#fecha' + self[i].numero).val(self[i].fechaReserva)
        }

    })

    validationInputSelects("form")
}

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

function verificar_cuota() {
    objeto = []
    objeto_inputs = $('.cuota')

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value

        if (h3 ==''){
            return {
                'numero': h1,
                'fechaVencimiento': false

            }

        }

    }


    return {
        'numero': h1,
        'fechaVencimiento': true

    }
}

function limpiar_label() {

    $('#label_cliente').html('')
    $('#label_urbanizacion').html('')
    $('#label_manzano').html('')
    $('#label_tipo_terreno').html('')
    $('#label_fecha_reserva').html('')
    $('#label_estado_reserva').html('')
    $('#label_monto').html('')
    $('#label_valor_metro2').html('')
    $('#label_superficie').html('')
    $('#label_valor_terreno').html('')
    $('#label_tasa_interes').html('')
    $('#label_interes').html('')
    $('#label_valor_credito').html('')

}

function cargar_reservas(idreserva) {
        obj = JSON.stringify({
        'idreserva': parseInt(idreserva),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "reserva_listar_para_contrato";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fkreserva').html('');
        var select = document.getElementById("fkreserva")
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = "Nº" + response['response'][i]['id'] +"  -  "+response['response'][i]['cliente']['fullname'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkreserva').selectpicker('refresh');
        

    })

}


$('#new').click(function () {
    id_gv = 0

    cargar_reservas(id_reserva)
    
    $('#fkreserva').val('')
    $('#fkreserva').selectpicker('refresh')


    $('#fktipoventa').val('')
    $('#fktipoventa').selectpicker('refresh')

    $('#fkentidad').val('')
    $('#fkentidad').selectpicker('refresh')


    $('#cuotaInicial').val('')
    $('#numeroCuotas').val('')
    $('#fechaPrimerCuota').val('')
    $('#cuota_div').empty()

    limpiar_label()


    verif_inputs('')
    validationInputSelects("form")

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})

$('#insert').click(function () {
    if (parseInt($('#numeroCuotas').val()) !=  parseInt($('.idcuota').length)){
        swal(
            'Error de datos.',
             'el numero de cuotas , no coincide con el numero de cuotas registradas',
            'warning'
        )
    }else{

        var verificarCuota = verificar_cuota()

        if(verificarCuota['fechaVencimiento'] == '')
        {
                swal(
                    'Cuota incompleta.',
                    'falta fecha vencimiento en la cuota ' + verificarCuota['numero'],
                    'warning'
                )

        }else{

            notvalid = validationInputSelectsWithReturn("form");
            if (notvalid===false) {

                objeto = JSON.stringify({
                    'cuotaInicial': $('#cuotaInicial').val(),
                    'fechaPrimerCuota': $('#fechaPrimerCuota').val(),
                    'fkreserva': $('#fkreserva').val(),
                    'fktipoventa': $('#fktipoventa').val(),
                    'fkentidad': $('#fkentidad').val(),
                    'numeroCuotas': $('#numeroCuotas').val(),
                    'capital': $('#label_valor_credito').text(),
                    'fkmoneda': $('#fkmoneda').val(),

                    'cuotas': get_cuota()

                })
                ajax_call('contrato_insert', {
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
    }
})

function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('contrato_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#fkcredito').val(self.fkcredito)

             cargar_reservas(self.fkreserva)

            $('#fkreserva').val(self.fkreserva)
            $('#fkreserva').selectpicker('refresh')

            cargar_detalle_reserva(self.fkreserva)

            $('#fktipoventa').val(self.fktipoventa)
            $('#fktipoventa').selectpicker('refresh')
            $('#fkentidad').val(self.credito.fkentidad)
            $('#fkentidad').selectpicker('refresh')

            $('#cuotaInicial').val(self.cuotaInicial)
            $('#numeroCuotas').val(self.numeroCuotas)
            $('#fechaPrimerCuota').val(self.fechaPrimerCuota)

            $('#cuota_div').empty()

            for (i in self.credito.cuotas) {

                append_input_cuota(self.credito.cuotas[i]['id'])

                $('#id' + self.credito.cuotas[i]['id']).val(self.credito.cuotas[i]['id'])
                $('#numero' + self.credito.cuotas[i]['id']).val(self.credito.cuotas[i]['numero'])
                $('#monto' + self.credito.cuotas[i]['id']).val(self.credito.cuotas[i]['monto'])
                $('#fecha' + self.credito.cuotas[i]['id']).val(self.credito.cuotas[i]['fechaVencimiento'])
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
        if (parseInt($('#numeroCuotas').val()) !=  parseInt($('.idcuota').length)){
        swal(
            'Error de datos.',
             'el numero de cuotas , no coincide con el numero de cuotas registradas',
            'warning'
        )
    }else{

        var verificarCuota = verificar_cuota()

        if(verificarCuota['fechaVencimiento'] == '')
        {
                swal(
                    'Cuota incompleta.',
                    'falta fecha vencimiento en la cuota ' + verificarCuota['numero'],
                    'warning'
                )

        }else{


            notvalid = validationInputSelectsWithReturn("form");
            if (notvalid===false) {
                objeto = JSON.stringify({
                    'id': parseInt($('#id').val()),
                    'fkcredito': parseInt($('#fkcredito').val()),
                    'cuotaInicial': $('#cuotaInicial').val(),
                    'fechaPrimerCuota': $('#fechaPrimerCuota').val(),
                    'fkreserva': $('#fkreserva').val(),
                    'fktipoventa': $('#fktipoventa').val(),

                    'fkentidad': $('#fkentidad').val(),
                    'numeroCuotas': $('#numeroCuotas').val(),
                    'capital': $('#label_valor_credito').text(),
                    'fkmoneda': $('#fkmoneda').val(),

                    'cuotas': get_cuota()

                })
                ajax_call('contrato_update', {
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
    }

})
reload_form()

function eliminar(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Venta?"

    } else {
        cb_title = "¿Habilitar Venta?"
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
        ajax_call('contrato_delete', {
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

