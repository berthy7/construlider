main_route = '/usuario'

$(document).ready(function () {
    $('.error').addClass("error-own");
});

validationKeyup("form")
validationSelectChange("form")
validationKeyup("form_usuarios")
validationSelectChange("form_usuarios")

$('.dd').nestable({
    group:'categories',
    maxDepth:0,
    reject: [{
        rule: function () {
            // The this object refers to dragRootEl i.e. the dragged element.
            // The drag action is cancelled if this function returns true
            var ils = $(this).find('>ol.dd-list > li.dd-item');
            for (var i = 0; i < ils.length; i++) {
                var datatype = $(ils[i]).data('type');
                if (datatype === 'child')
                    return true;
            }
            return false;
        },
        action: function (nestable) {
            // This optional function defines what to do when such a rule applies. The this object still refers to the dragged element,
            // and nestable is, well, the nestable root element
            alert('Can not move this item to the root');
        }
    }]
});

$('.module').click(function () {
    var checked = $(this).prop('checked')
    //$('.module').prop('checked', false)
    empresa_id = null
    sucursal_id = null
    gerencia_id = null
    grupo_id = null
    emp_id = null
    if ($(this).hasClass('employee')){
        emp_id = parseInt($(this).attr('data-id'))
    } else {
        if ($(this).hasClass('grupo')){
            grupo_id = parseInt($(this).attr('data-id'))
            gerencia_id = parseInt($(this).attr('data-ger'))
            sucursal_id = parseInt($(this).attr('data-suc'))
            empresa_id = parseInt($(this).attr('data-empr'))
        } else {
            if ($(this).hasClass('gerencia')){
                gerencia_id = parseInt($(this).attr('data-id'))
                sucursal_id = parseInt($(this).attr('data-suc'))
                empresa_id = parseInt($(this).attr('data-empr'))
            }else {
                if($(this).hasClass('sucursal')){
                    sucursal_id = parseInt($(this).attr('data-id'))
                    empresa_id = parseInt($(this).attr('data-empr'))
                }else {
                    if($(this).hasClass('empresa')){
                        empresa_id_id = parseInt($(this).attr('data-id'))
                    }
                }
            }
        }
    }
    $(this).prop('checked', checked)
    $(this).parent().next().find('.module').prop('checked', $(this).prop('checked'))
    analizar($(this).parent().parent().closest('.dd-list').prev().find('.module'))
})

function analizar(parent) {
    children = $(parent).parent().next().find('.module:checked')
    //console.log(children.length)
    $(parent).prop('checked', (children.length > 0))
    grand_parent = $(parent).parent().parent().closest('.dd-list').prev().find('.module')
    //console.log(grand_parent.length)
    if (grand_parent.length > 0){
        analizar(grand_parent)
    }
}



$('#fkrol').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar perfil.',
    title: 'Seleccione un perfil.'
})

$('#fkresidente').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar residente',
    title: 'Seleccione residente'
})

$('#fkcondominio').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar condominio',
    title: 'Seleccione condominio'
})

$('#expendido').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

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
        "order": [[ 1, "desc" ]],
        language : {
            'url': '/resources/js/spanish.json',
        },
        "pageLength": 50
    });
}

attach_validators()


$('#new').click(function () {
    $('#id').val('')
    $('#nombre_usuario').val('')
    $('#apellidop').val('')
    $('#apellidom').val('')
    $('#telefono').val('')
    $('#username').val('')
    $('#password').val('')
    $('#correo').val('')
    $('#ci').val('')
    $('#expendido').val('')
    $('#expendido').selectpicker('refresh')

    $('#fkrol').val('')
    $('#fkrol').selectpicker('refresh')
    

    verif_inputs('')
    validationInputSelects("form")
    $('#id_div').hide()
    $('#insert').show()
    $('#pass').show()
    $('#update').hide()
    $('#div_username').hide()

    $('#form').modal('show')
})

$('#generar').click(function () {

    swal({
        title: "¿Restablecer contraseña?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#393939",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
            objeto = JSON.stringify({
             'idusuario': parseInt($('#id').val()),
             'password': $('#ci').val()
    
            })
            ajax_call_asincrono('usuario_restablecer_password', {
                _xsrf: getCookie("_xsrf"),
                object: objeto
            }, null, function (response) {
                response = JSON.parse(response);
                if(response.success === true){
                    swal(
                          'Actualizada Correctamente.',
                          '',
                          'success'
                    )
                    $('#password').val($('#ci').val())
                    
                }else{
    
                    swal(
                        'Datos duplicados',
                        response.message,
                        'error'
                    )
                }
    
            })
        

        
    })



})


$('#insert').click(function () {
    if(!validationInputSelects("form")){

        objeto = JSON.stringify({
         'nombre': $('#nombre_usuario').val(),
        'apellidop': $('#apellidop').val(),
        'apellidom': $('#apellidom').val(),
        'telefono': $('#telefono').val(),
        'username': $('#username').val(),
        'password': $('#password').val(),
        'fkrol': parseInt($('#fkrol').val()),
        'ci': $('#ci').val(),
        'correo': $('#correo').val(),
        'expendido': $('#expendido').val()

        })

        objeto_verificar = JSON.stringify({
            'username': $('#correo').val(),
        })
        
        ajax_call_post("usuario_verificar_username", {
            _xsrf: getCookie("_xsrf"),
            object: objeto_verificar
        }, function (response) {
            if(response.success === true){
                ajax_call_asincrono('usuario_insert', {
                    _xsrf: getCookie("_xsrf"),
                    object: objeto
                }, null, function (response) {
                    response = JSON.parse(response);
                    if(response.success === true){
        
                        var data = [];
                        var id
                        var estado
                        for (var i = 0; i < Object.keys(response.response).length; i++) {
                            id = response['response'][i]['id']
                            estado = response['response'][i]['enabled']
                            if(estado == true){
                                estado = "<input id='" + id + "' onClick='event.preventDefault();eliminar(this)' data-id='" + id + "' type='checkbox' class='chk-col-indigo 'checked disabled/><label for='" + id + "'></label>" +" "+ "Habilitado"

                            }else{
                                estado = "<input id='" + id + "' onClick='event.preventDefault();eliminar(this)'data-id='" + id + "' type='checkbox' class='chk-col-indigo ' disabled/><label for='" + id + "'></label>" + " " + "Deshabilitado"

                            }
                            data.push( [
                                response['response'][i]['fullname'],
                                response['response'][i]['username'],
                                response['response'][i]['rol']['nombre'],
                                estado,
                                "<button id='edit' onClick='editar(this)' data-json='" + id + "' type='button' class='btn bg-indigo waves-effect waves-light edit' title='Editar'><i class='material-icons'>create</i></button>"
                            ]);
                        }
        
                        cargar_tabla(data)
                    }else{
        
                        swal(
                            'Datos duplicados',
                            response.message,
                            'error'
                        )
                    }
        
                })
                showMessage("Insertado Correctamente", "success", "ok")
                $('#form').modal('hide')

            }else{
                swal(
                    'Correo en uso',
                    'El correo ya se encuentra, en uso porfavor, ingrese otro correo electronico',
                    'warning' )
            }
        });

    }else{
        swal(
            'Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
})

function editar(elemento){
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(elemento).attr('data-json')))
    })
    ajax_call_get('usuario_update', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response;

        $('#id').val(self.id),
        $('#nombre_usuario').val(self.nombre),
        $('#apellidop').val(self.apellidop),
        $('#apellidom').val(self.apellidom),
        $('#telefono').val(self.telefono),
        $('#ci').val(self.ci)
        $('#correo').val(self.correo)
        $('#expendido').val(self.expendido)
        $('#expendido').selectpicker('refresh')

        $('#username').val(self.username)
        $('#password').val('')
        $('#fkrol').val(self.fkrol)
        $('#fkrol').selectpicker('render')

        validationInputSelects("form")
        verif_inputs('')
        $('#id_div').hide()
        $('#insert').hide()
        $('#update').show()
        $('#pass').hide()
        $('#div_username').show()
        $('#form').modal('show')
    })
    }


$('#update').click(function () {
    objeto = JSON.stringify({
        'id': parseInt($('#id').val()),
        'nombre': $('#nombre_usuario').val(),
        'apellidop': $('#apellidop').val(),
        'apellidom': $('#apellidom').val(),
        'telefono': $('#telefono').val(),
        'username': $('#username').val(),
        'password': $('#password').val(),
         'ci': $('#ci').val(),
         'correo': $('#correo').val(),
         'expendido': $('#expendido').val(),
        'fkrol': parseInt($('#fkrol').val())
    })

    objeto_verificar = JSON.stringify({
        'username': $('#username').val(),

    })

    ajax_call_post("usuario_verificar_username", {
        _xsrf: getCookie("_xsrf"),
        object: objeto_verificar
    }, function (response) {
        if(response.success === true){

        ajax_call('usuario_update', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function (response) {
            response = JSON.parse(response);
            if(response.success === true){
                var data = [];
                var id
                var estado
                for (var i = 0; i < Object.keys(response.response).length; i++) {
                    id = response['response'][i]['id']
                    estado = response['response'][i]['enabled']
                    if(estado == true){
                        estado = "<input id='" + id + "' onClick='event.preventDefault();eliminar(this)' data-id='" + id + "' type='checkbox' class='chk-col-indigo 'checked disabled/><label for='" + id + "'></label>" +" "+ "Habilitado"

                    }else{
                        estado = "<input id='" + id + "' onClick='event.preventDefault();eliminar(this)'data-id='" + id + "' type='checkbox' class='chk-col-indigo ' disabled/><label for='" + id + "'></label>" + " " + "Deshabilitado"

                    }
                    data.push( [
                        response['response'][i]['fullname'],
                        response['response'][i]['username'],
                        response['response'][i]['rol']['nombre'],
                        estado,
                        "<button id='edit' onClick='editar(this)' data-json='" + id + "' type='button' class='btn bg-indigo waves-effect waves-light edit' title='Editar'><i class='material-icons'>create</i></button>"
                    ]);
                }

                cargar_tabla(data)
            }else{

                swal(
                    'Datos duplicados',
                    response.message,
                    'error'
                )
            }

        })
        showMessage("Modificado Correctamente", "success", "ok")
        $('#form').modal('hide')

        }else{
            swal(
                'Nombre de usuario en uso',
                'Por favor ingrese otro nombre de usuario',
                'warning' )
        }
    });

})
reload_form()
$('#role_id').selectpicker()


var verificar = false
idu = 0

function eliminar(elemento){
    cb_delete = elemento
    b = $(elemento).prop('checked')
    if (!b) {
        cb_title = "¿Deshabilitar Usuario?"

    } else {
        cb_title = "¿Habilitar Usuario?"
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
        ajax_call('usuario_delete', {
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

$('#modificar_password').on('shown.bs.modal', function () {
    $('#new_pass').focus();
})


$('.reset').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))

    $('#new_pass').val('')
    $('#new_rpass').val('')
    $('#new_pass').parent().addClass('focused')
    $('#new_rpass').parent().addClass('focused')
    $('#actual_pass').focus()
    $('#id_usuario').val(id)
    $('#modificar_password').modal('show');
})


function Modificar_Contraseña() {
    values="new_pass,new_rpass";

    if(validate_inputs_empty(values)) {
        swal({
            title: "Desea modificar la contraseña al usuario?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#4CAF50",
            cancelButtonColor: "#F44336",
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar"
        }).then(function () {
            id = $('#id_usuario').val()
            newp = $('#new_pass').val()
            newp1 = $('#new_rpass').val()
            objeto =JSON.stringify({'id' : id,'new_password' : newp, 'new_password_2':newp1})

            if(newp==newp1) {
                $.ajax({
                    url: "/usuario_reset_password",
                    type: "post",
                    data: {object:objeto, _xsrf: getCookie("_xsrf")},
                }).done(function (response) {
                    valor=JSON.parse(response)
                    if(valor.success) {
                        swal(
                            'Contraseña modificada.',
                            'Se modificó la contraseña correctamente.',
                            'success'
                        )
                    } else {
                        swal(
                            'Contraseña actual errónea.',
                            'No se modificó la contraseña.',
                            'error'
                        )
                    }
                })
            } else {
                swal(
                    'Error de datos.',
                    'Las contraseñas no coinciden.',
                    'error'
                )
            }
        })
    } else {
        swal(
            'Error de datos.',
            'Hay campos vacíos por favor verifique sus datos.',
            'error'
        )
    }
}


$('.reset1').click(function () {
    id = parseInt(JSON.parse($(this).attr('data-json')))

    swal({
        title: "Desea anular el dispositivo y habilitar nuevamente al usuario?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#1565c0",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        cancelButtonText: "Cancelar"
    }).then(function () {
        ajax_call("/usuario_codigo_reset", { id: id,_xsrf: getCookie("_xsrf")}, null, function () {setTimeout(function(){window.location=main_route}, 2000);})
    })
})