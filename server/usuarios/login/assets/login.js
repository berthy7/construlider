$( document ).ready(function() { });

$(function () {
    $('#sign_in').validate({
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.input-group').append(error);
        }
    });
});

$('#see-pass').mousedown(function(){
    $("#ic-pass").css("color", "lightgrey");
    $("#password").prop("type", "text");
    $("#ic-pass").html("visibility");
});

$("#see-pass").mouseup(function(){
    $("#ic-pass").css("color", "grey");
    $("#password").prop("type", "password");
    $("#ic-pass").html("visibility_off");
});

function validar(){
    if($('#username').val() == '' && $('#password').val() == ''){
        $('#msg-data').fadeIn('slow')
        return false
    }else{
        $('#msg-data').fadeOut('slow')
        return true
    }
}

$('#sign_in').submit(function(){
    if(!$('#username').val() == '' && $(!'#password').val() == ''){
        $('#btn-login').html('Espere...')
        $('#msg-data').fadeOut('slow')
    }else{
        $('#msg-data').fadeIn('slow')
    }
});