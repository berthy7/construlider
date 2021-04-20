main_route = '/devolucion'

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
        "order": [[ 0, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}



function reporte_pdf(elemento){

    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
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
}

function reporte_excel(elemento){

    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
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
    $('#modal-rep-xls').modal('show')
}

$('#update').click(function () {
    notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fechaReserva': $('#fechaReserva').val(),
            'monto': $('#monto').val(),
            'fkcliente': $('#fkcliente').val(),
            'fkterreno': $('#fkterreno').val(),
            'fkestadodevolucion': $('#fkestadodevolucion').val()
            
        })
        ajax_call('devolucion_update', {
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
    ajax_call_get('devolucion_update', {
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
            $('#label_fecha_devolucion').html(self.fechaReserva)
            $('#label_monto').html(self.monto)
            $('#label_estado_devolucion').html(self.estadodevolucion.nombre)

            clean_form()
            verif_inputs('')
            validationInputSelects("form_cancelar")
            $('#id_div_cancelar').hide()
            $('#boton_cancel').show()
            $('#boton_cerrar').hide()
            $('#form_cancelar').modal('show')
    })
    }

$('#boton_cancel').click(function () {

    objeto = JSON.stringify({
        'id': parseInt($('#id_cancelar').val())
    })
    ajax_call('devolucion_cancel', {
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
        ajax_call('devolucion_delete', {
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
        url: "/devolucion_reporte_xls",
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
        url: '/devolucion_reporte_pdf',
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

