main_route = '/manzano'

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
                targets: 5,
                className: 'text-center'
            },
            {
                targets: 6,
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

function append_input_terreno(id_in) {

    $('#terreno_div').append(
    '<div class="row">\
        <div class="col-sm-1 hidden">\
            <div class="input-group">\
            <input  id="id'+id_in+'" class="form-control  idterreno reserva readonly txta-own">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div class="form-line">\
            <input  id="ancho'+id_in+'" type="number" class="form-control reserva txta-own">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div class="form-line">\
                <input id="largo'+id_in+'" type="number" data-id="'+id_in+'" class="form-control reserva  txta-own">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div  class="form-line">\
                <input id="superficie'+id_in+'" type="number" data-id="'+id_in+'" class="form-control reserva  txta-own">\
            </div>\
        </div>\
        <div class="col-sm-3">\
            <div  class="form-line">\
                <input id="superficieConstruida'+id_in+'" type="number" data-id="'+id_in+'" class="form-control reserva  txta-own">\
            </div>\
        </div>\
        <div class="col-sm-1">\
            <button type="button" class="btn bg-red waves-effect clear_" title="Eliminar">\
                <i class="material-icons">clear</i>\
            </button>\
        </div>\
    </div>'
)

    $('.clear_').last().click(function () {
        $(this).parent().parent().remove()
    })


}

$('#new_terreno').click(function () {

       append_input_terreno('')

})

function get_terreno() {
    objeto = []
    objeto_inputs = $('.reserva')

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


$('#fkurbanizacion').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})



$('#new').click(function () {
    $('#numero').val('')
    $('#calle1').val('')
    $('#calle2').val('')
    $('#fkurbanizacion').val('')
    $('#fkurbanizacion').selectpicker('refresh')

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
            'numero': $('#numero').val(),
            'calle1': $('#calle1').val(),
            'calle2': $('#calle2').val(),
            'fkurbanizacion': $('#fkurbanizacion').val()
         
        })
        ajax_call('manzano_insert', {
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
    ajax_call_get('manzano_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#numero').val(self.numero)
            $('#calle1').val(self.calle1)
            $('#calle2').val(self.calle2)
            $('#fkurbanizacion').val(self.fkurbanizacion)
            $('#fkurbanizacion').selectpicker('refresh')

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
            'numero': $('#numero').val(),
            'calle1': $('#calle1').val(),
            'calle2': $('#calle2').val(),
            'fkurbanizacion': $('#fkurbanizacion').val()
            
        })
        ajax_call('manzano_update', {
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
        cb_title = "¿Deshabilitar Manzano?"

    } else {
        cb_title = "¿Habilitar Manzano?"
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
        ajax_call('manzano_delete', {
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

