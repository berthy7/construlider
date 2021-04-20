main_route = '/ajuste'

$(document).ready(function () {
 cargar_reserva_minima()
});


$(document).ajaxStart(function () { });

$(document).ajaxStop(function () {
    $.Toast.hideToast();
});

function cargar_reserva_minima(){

    $('#fkmonedaReserva').val($('#input_fkmonedaReserva').val())
    $('#fkmonedaReserva').selectpicker('refresh');

}

$('#actualizarReserva').click(function () {

    objeto = JSON.stringify({
        'montoMinimoReserva': $('#montoMinimoReserva').val(),
        'fkmonedaReserva': $('#fkmonedaReserva').val()
    })
    ajax_call('ajuste_update', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })

})


$('#actualizarTasaInteres').click(function () {

    objeto = JSON.stringify({
        'tasaInteres': $('#tasaInteres').val()
    })
    ajax_call('ajuste_update', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })

})

$('#actualizarcuotasMora').click(function () {

    objeto = JSON.stringify({
        'cuotasMora': $('#cuotasMora').val()
    })
    ajax_call('ajuste_update', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        setTimeout(function () {
            window.location = main_route
        }, 2000);
    })

})


reload_form()




validationKeyup("form")
validationSelectChange("form")

