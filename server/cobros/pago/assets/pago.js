main_route = '/pago'

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

$('#fkcliente').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione Cliente'
})

$('#fkcredito').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione Credito'
})

$('#fktipopago').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione tipo pago'
})

$('#fkcliente').change(function () {

    cargar_creditos($('#fkcliente').val())

});

function cargar_creditos(idcliente) {

    obj = JSON.stringify({
        'idcliente': parseInt(idcliente),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "credito_listar_x_cliente";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fkcredito').html('');
        var select = document.getElementById("fkcredito")
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = "Nº" + response['response'][i]['id']+" - "+ response['response'][i]['capital']+" "+ response['response'][i]['moneda']['codigo'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkcredito').selectpicker('refresh');

        $('#label_numero_cuota').html(self.valorCredito)
        $('#label_monto_cuota').html(self.valorCredito)
        $('#label_fecha_vencimiento').html(self.valorCredito)



    })

}

$('#fkcredito').change(function () {

    cargar_cuota_x_pagar($('#fkcredito').val())

});

function cargar_cuota_x_pagar(idcredito) {

    obj = JSON.stringify({
        'id': parseInt(idcredito),
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_get('pago_obtener_cuota_x_pagar', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#fkcuota').val(self.idCuota)
            $('#label_numero_cuota').html(self.numeroCuota)
            $('#label_monto_cuota_inicial').html(self.montoCuota)
            $('#label_monto_cuota_parcial').html(self.montoCuotaParcial)
            $('#label_fecha_vencimiento').html(self.fechaVencimiento)
            $('#label_estado_cuota').html(self.estadoCuota)
            $('.moneda').html(self.moneda)
            

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

function append_input_cuota(id_in,monto) {

    if(id_in === ''){
        id_gv++;
        id_in = id_gv;
    }


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
                <input id="monto'+id_in+'" value="'+monto+'" class="form-control cuota  txta-own">\
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
    parent_div = document.getElementById('cuota_div');
    current_cant = $(parent_div).children().length;
    cant_create = document.getElementById('numeroCuotas').value !== ''? parseInt(document.getElementById('numeroCuotas').value): 0;
    dif_cant = cant_create - current_cant;

    obj = JSON.stringify({
        'valorCredito': parseInt($('#label_valor_credito').text()),
        'numeroCuotas': parseInt($('#numeroCuotas').val()),
        '_xsrf': getCookie("_xsrf")
    })

    ajax_call_get('pago_valor_cuota', {
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

$('#importar_Excel').click(function () {
    $(".xlsfl").each(function () {
        $(this).fileinput('refresh',{
            allowedFileExtensions: ['xlsx', 'txt'],
            maxFileSize: 2000,
            maxFilesNum: 1,
            showUpload: false,
            layoutTemplates: {
                main1: '{preview}\n' +
                    '<div class="kv-upload-progress hide"></div>\n' +
                    '<div class="input-group {class}">\n' +
                    '   {caption}\n' +
                    '   <div class="input-group-btn">\n' +
                    '       {remove}\n' +
                    '       {cancel}\n' +
                    '       {browse}\n' +
                    '   </div>\n' +
                    '</div>',
                main2: '{preview}\n<div class="kv-upload-progress hide"></div>\n{remove}\n{cancel}\n{browse}\n',
                preview: '<div class="file-preview {class}">\n' +
                    '    {close}\n' +
                    '    <div class="{dropClass}">\n' +
                    '    <div class="file-preview-thumbnails">\n' +
                    '    </div>\n' +
                    '    <div class="clearfix"></div>' +
                    '    <div class="file-preview-status text-center text-success"></div>\n' +
                    '    <div class="kv-fileinput-error"></div>\n' +
                    '    </div>\n' +
                    '</div>',
                icon: '<span class="glyphicon glyphicon-file kv-caption-icon"></span>',
                caption: '<div tabindex="-1" class="form-control file-caption {class}">\n' +
                    '   <div class="file-caption-name"></div>\n' +
                    '</div>',
                btnDefault: '<button type="{type}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</button>',
                btnLink: '<a href="{href}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</a>',
                btnBrowse: '<div tabindex="500" class="{css}"{status}>{icon}{label}</div>',
                progress: '<div class="progress">\n' +
                    '    <div class="progress-bar progress-bar-success progress-bar-striped text-center" role="progressbar" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100" style="width:{percent}%;">\n' +
                    '        {percent}%\n' +
                    '     </div>\n' +
                    '</div>',
                footer: '<div class="file-thumbnail-footer">\n' +
                    '    <div class="file-caption-name" style="width:{width}">{caption}</div>\n' +
                    '    {progress} {actions}\n' +
                    '</div>',
                actions: '<div class="file-actions">\n' +
                    '    <div class="file-footer-buttons">\n' +
                    '        {delete} {other}' +
                    '    </div>\n' +
                    '    {drag}\n' +
                    '    <div class="file-upload-indicator" title="{indicatorTitle}">{indicator}</div>\n' +
                    '    <div class="clearfix"></div>\n' +
                    '</div>',
                actionDelete: '<button type="button" class="kv-file-remove {removeClass}" title="{removeTitle}"{dataUrl}{dataKey}>{removeIcon}</button>\n',
                actionDrag: '<span class="file-drag-handle {dragClass}" title="{dragTitle}">{dragIcon}</span>'
            }
        })
    });
    verif_inputs('')

    $('#id_div').hide()
    $('#insert-importar').show()
    $('#form-importar').modal('show')
})

$('#new').click(function () {
    id_gv = 0
    $('#monto').val('')
    $('#fecha').val('')
    $('#fkmoneda').val(2)
    $('#fkmoneda').selectpicker('refresh')
    $('#fkcuota').val('')
    $('#fkcliente').val('')
    $('#fkcliente').selectpicker('refresh')

    $('#fkcredito').val('')
    $('#fkcredito').selectpicker('refresh')

    $('#fktipopago').val('')
    $('#fktipopago').selectpicker('refresh')

    $('#fotoComprobante').fileinput('clear');

    verif_inputs('')
    validationInputSelects("form")

    $('#id_div').hide()
    $('#insert').show()
    $('#update').hide()
    $('#form').modal('show')
})

$('#insert').on('click',function (e) {
     e.preventDefault();
     notvalid = validationInputSelectsWithReturn("form");
    if (notvalid===false) {
        var data = new FormData($('#form_submit')[0]);

        objeto = JSON.stringify({
            'monto': $('#monto').val(),
            'fkmoneda': $('#fkmoneda').val(),
            'fkcuota': $('#fkcuota').val(),
            'fktipopago': $('#fktipopago').val(),
            'montoCuotaParcial': $('#label_monto_cuota_parcial').text(),

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
            url: 'pago_insert',
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
            setTimeout(function () {
                window.location = main_route
            }, 2000);
        $('#form').modal('hide')

        
    } else {
        swal(
            'Error de datos.',
             notvalid,
            'warning'
        )
    }
})

function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('pago_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#monto').val(self.monto)
            $('#fkmoneda').val(self.fkmoneda)
            $('#fkcuota').val(self.fkcuota)
            $('#fktipopago').val(self.fktipopago)
            $('#fktipopago').selectpicker('refresh')

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
            'monto': $('#monto').val(),
            'fkmoneda': $('#fkmoneda').val(),
            'fkcuota': $('#fkcuota').val(),
            'fktipopago': $('#fktipopago').val()
            
        })
        ajax_call('pago_update', {
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
        cb_title = "¿Deshabilitar Pago?"

    } else {
        cb_title = "¿Habilitar Pago?"
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
        ajax_call('pago_delete', {
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

