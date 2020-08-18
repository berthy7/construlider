$(document).ready(function () {
    $.extend( true, $.fn.dataTable.defaults, {
        "language": {
            "url": "resources/js/spanish.json"
        },
        dom: '<"pull-left"f><"pull-right"l>tip',

    } );


    let pathname = window.location.pathname; //URL de la página
    let a = document.querySelector("a[href='"+pathname+"']");
    let b = (a.parentNode).parentNode; //tiene LI
    let c = b.previousElementSibling; //tiene a href, elemento anterior a LI
    if (c == null){
        b.style["display"] = "block";
    }else{
        c.classList.add('toggled');
        b.style["display"] = "block";
        a.style["background-color"] = "rgba(0,0,0,.2)";
    }

});

function  Salir() {
    swal({
        title: "¿Desea cerrar sesión?",
        imageUrl: 'resources/iconos/logo_python.jpg',
        showCancelButton: true,
        confirmButtonColor: "#393939",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        reverseButtons: true,
        cancelButtonText: "Cancelar"
    }).then(function () {
        swal(
              'Gracias por tu trabajo.',
              'Vuelve pronto.',
              'success'
        )
        setTimeout(function () {
            window.location="/logout"
        }, 700);
    })
}

$('.datei').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    $('#fechaf').bootstrapMaterialDatePicker('setMinDate', date);
    if($('#fechai').val() > $('#fechaf').val()){

        $('#fechaf').val($('#fechai').val());
    }


});

$('.datef').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');

    if($('#fechaf').val() < $('#fechai').val()){
        $('#fechaf').bootstrapMaterialDatePicker('setMinDate', date);
        $('#fechaf').val($('#fechai').val());

    }

});

