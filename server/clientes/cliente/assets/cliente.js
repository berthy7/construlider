main_route = '/cliente'

$(document).ready(function () {});

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
                targets: 3,
                className: 'text-center'
            },
            {
                targets: 4,
                className: 'text-center'
            }
          ],

        "order": [[ 2, "asc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 25
    });
}

$('#new').click(function () {
    $('#nombre').val('')
    $('#apellidos').val('')
    $('#carnet').val('')
    $('#telefono').val('')
    $('#email').val('')


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
            'nombre': $('#nombre').val(),
            'apellidos': $('#apellidos').val(),
            'carnet': $('#carnet').val(),
            'telefono': $('#telefono').val(),
            'email': $('#email').val()
         
        })
        ajax_call('cliente_insert', {
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

function editar(elemento) {
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('cliente_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;
        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $('#apellidos').val(self.apellidos)
        $('#carnet').val(self.carnet)
        $('#telefono').val(self.telefono)
        $('#email').val(self.email)


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
            'nombre': $('#nombre').val(),
            'apellidos': $('#apellidos').val(),
            'carnet': $('#carnet').val(),
            'telefono': $('#telefono').val(),
            'email': $('#email').val()
            
        })
        ajax_call('cliente_update', {
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

function eliminar(elemento) {
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Cliente?"

    } else {
        cb_title = "¿Habilitar Cliente?"
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
        ajax_call('cliente_delete', {
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

