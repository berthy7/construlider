main_route = '/reserva';


id_terreno = null;

var var_montoMinimoReserva;
var var_monedaReserva;



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

var fechahoy = new Date();
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()

document.getElementById("fechaReserva").value=hoy

function cargar_reserva_minima(montoMinimoReserva,fkmonedaReserva) {

    var_montoMinimoReserva = montoMinimoReserva;
    var_monedaReserva = fkmonedaReserva;

    $('#monto').val(montoMinimoReserva)
    $('#fkmoneda').val(fkmonedaReserva)
    $('#fkmoneda').selectpicker('refresh');


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
                targets: 9,
                className: 'text-center'
            },
            {
                targets: 10,
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
    title: 'Seleccione urbanizacion'
})

$('#fkmanzano').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione manzano'
})

$('#fkcliente').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione cliente'
})

$('#fktipoTerreno').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione tipo terreno'
})

$('#fkterreno').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione terreno'
})

$('#fkestadoreserva').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione estado reserva'
})

$('#fkurbanizacion').change(function () {

    cargar_manzanos($('#fkurbanizacion').val())

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
            var option = document.createElement("OPTION");
            option.innerHTML = "Nº" + response['response'][i]['numero'] +"  -  "+response['response'][i]['calle1'] +":"+response['response'][i]['calle2'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkmanzano').selectpicker('refresh');

        $('#fktipoTerreno').val('');
        $('#fktipoTerreno').selectpicker('refresh');

        $('#fkterreno').html('');
        $('#fkterreno').selectpicker('refresh');

    })

}

$('#fktipoTerreno').change(function () {

    cargar_terrenos($('#fkmanzano').val(),$('#fktipoTerreno').val(),id_terreno)

});

$('#fkmanzano').change(function () {

    cargar_terrenos($('#fkmanzano').val(),$('#fktipoTerreno').val(),id_terreno)

});

function cargar_terrenos(idmanzano,idtipoterreno,idterreno) {
        obj = JSON.stringify({
        'idmanzano': parseInt(idmanzano),
        'idtipoterreno': parseInt(idtipoterreno),
        'idterreno': parseInt(idterreno),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "terreno_listar_x_tipo";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fkterreno').html('');
        var select = document.getElementById("fkterreno")
        var sc = ""
        for (var i = 0; i < Object.keys(response.response).length; i++) {


            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['id'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkterreno').selectpicker('refresh');

    })

}

$('#new').click(function () {
    id_terreno = null;
    $('#fkcliente').val('')
    $('#fkcliente').selectpicker('refresh')
    $('#fkurbanizacion').val('')
    $('#fkurbanizacion').selectpicker('refresh')
    $('#fkmanzano').val('')
    $('#fkmanzano').selectpicker('refresh')
    $('#fktipoTerreno').val('')
    $('#fktipoTerreno').selectpicker('refresh')
    $('#fkterreno').val('')
    $('#fkterreno').selectpicker('refresh')
    $('#fkestadoreserva').val('')
    $('#fkestadoreserva').selectpicker('refresh')

    verif_inputs('')
    validationInputSelects("form")

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})

$('#insert').click(function () {


    if (parseInt($('#monto').val()) >=  var_montoMinimoReserva){


        if (parseInt($('#fkmoneda').val()) === parseInt(var_monedaReserva)){
            notvalid = validationInputSelectsWithReturn("form");
            if (notvalid===false) {
                objeto = JSON.stringify({
                    'fechaReserva': $('#fechaReserva').val(),
                    'monto': $('#monto').val(),
                    'fkmoneda': $('#fkmoneda').val(),
                    'fkcliente': $('#fkcliente').val(),
                    'fkterreno': $('#fkterreno').val(),
                    'fkestadoreserva': $('#fkestadoreserva').val()
                })
                ajax_call('reserva_insert', {
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

        }else{
            swal(
                'Error de moneda.',
                 'el valor ingresado no coincide con la moneda requisito ',
                'warning'
            )

        }

    }else{
        swal(
            'Error de monto.',
             'el valor ingresado no supera el monto de reserva minimo',
            'warning'
        )

    }
})

function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('reserva_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#fechaReserva').val(self.fechaReserva)
            $('#monto').val(self.monto)
            $('#fkmoneda').val(self.fkmoneda)
            $('#fkmoneda').selectpicker('refresh');
            $('#fkcliente').val(self.fkcliente)
            $('#fkcliente').selectpicker('refresh');
            $('#fkurbanizacion').val(self.terreno.manzano.fkurbanizacion)
            $('#fkurbanizacion').selectpicker('refresh');

            cargar_manzanos(self.terreno.manzano.fkurbanizacion)

            $('#fkmanzano').val(self.terreno.fkmanzano)
            $('#fkmanzano').selectpicker('refresh');

            $('#fktipoTerreno').val(self.terreno.fktipoterreno)
            $('#fktipoTerreno').selectpicker('refresh');

            id_terreno = self.fkterreno
            cargar_terrenos(self.terreno.fkmanzano,self.terreno.fktipoterreno,id_terreno)

            $('#fkterreno').val(id_terreno)
            $('#fkterreno').selectpicker('refresh');

            $('#fkestadoreserva').val(self.fkestadoreserva)
            $('#fkestadoreserva').selectpicker('refresh');



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
            'fechaReserva': $('#fechaReserva').val(),
            'monto': $('#monto').val(),
            'fkmoneda': $('#fkmoneda').val(),
            'fkcliente': $('#fkcliente').val(),
            'fkterreno': $('#fkterreno').val(),
            'fkestadoreserva': $('#fkestadoreserva').val()
            
        })
        ajax_call('reserva_update', {
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

function cancelar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('reserva_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id_cancelar').val(self.id)
            $('#fechaReserva').val(self.fechaReserva)
            $('#monto').val(self.monto)
            $('#label_cliente').html(self.cliente.fullname)
            $('#label_urbanizacion').html(self.terreno.manzano.urbanizacion.direccion)
            $('#label_manzano').html(self.terreno.manzano.calle1)
            $('#label_tipo_terreno').html(self.terreno.tipoterreno.nombre)
            $('#label_fecha_reserva').html(self.fechaReserva)
            $('#label_monto').html(self.monto)
            $('#label_estado_reserva').html(self.estadoreserva.nombre)

            clean_form()
            verif_inputs('')
            validationInputSelects("form_cancelar")
            $('#id_div_cancelar').hide()
            $('#boton_cancel').show()
            $('#boton_cerrar').hide()
            $('#form_cancelar').modal('show')
    })
}

$('#boton_cerrar').click(function () {

    $('#form_cancelar').modal('hide')
    setTimeout(function () {
        window.location = main_route
    }, 1000);

})

$('#boton_cancel').click(function () {

    objeto = JSON.stringify({
        'id': parseInt($('#id_cancelar').val())
    })
    ajax_call('reserva_cancel', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {

    })
    $('#boton_cancel').hide()
    $('#boton_cerrar').show()
    $('#reportes').show()

})
reload_form()

function eliminar(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Reserva?"

    } else {
        cb_title = "¿Habilitar Reserva?"
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
        ajax_call('reserva_delete', {
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

$('#reporte-xls').click(function () {
    $('#exportar_excel').show()

    obj = JSON.stringify({
        'id': parseInt($('#id_cancelar').val())
    })

    $.ajax({
        method: "POST",
        url: "/reserva_reporte_xls",
        data:{_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function(response){
        response = JSON.parse(response)

        if (response.success) {
            $('#link_excel').attr('href', response.response.url).html(response.response.nombre)
        }
    })
    // $('#modal-rep-xls').modal('show')
})

 $('#reporte-pdf').click(function () {

    obj = JSON.stringify({
        'id': parseInt($('#id_cancelar').val())
    })

    $.ajax({
        method: "POST",
        url: '/reserva_reporte_pdf',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)

        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
})

validationKeyup("form")
validationSelectChange("form")

