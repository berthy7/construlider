main_route = '/terreno'

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

$('#fkmanzano').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
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
            option.innerHTML = response['response'][i]['numero'] +" - "+response['response'][i]['calle1'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkmanzano').selectpicker('refresh');

    })

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
        ajax_call('terreno_insert', {
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
    ajax_call_get('terreno_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
            $('#id').val(self.id)
            $('#ancho').val(self.ancho)
            $('#largo').val(self.largo)
            $('#superficie').val(self.superficie)
            $('#fkurbanizacion').val(self.manzano.fkurbanizacion)
            $('#fkurbanizacion').selectpicker('refresh')

            cargar_manzanos($('#fkurbanizacion').val())

            $('#fkmanzano').val(self.fkmanzano)
            $('#fkmanzano').selectpicker('refresh')

        
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
            'ancho': $('#ancho').val(),
            'largo': $('#largo').val(),
            'superficie': $('#superficie').val(),
            'fkmanzano': $('#fkmanzano').val()
            
        })
        ajax_call('terreno_update', {
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
        cb_title = "¿Deshabilitar Terreno?"

    } else {
        cb_title = "¿Habilitar Terreno?"
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
        ajax_call('terreno_delete', {
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

