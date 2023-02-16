
$(document).ready(function(){

    var email = $('[name="email"]');
    email.keyup(function(){
        $.ajax({
            type: 'POST',
            url: '/check-email',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: JSON.stringify({
                'email': email.val(),
            }),
            success: function(data){
                email.removeClass('is-invalid');
                email.addClass('is-valid');
                $('#submitBtn').prop('disabled', false);
            },
            error: function(jqXHR){
                switch (jqXHR.status){
                    case 409:
                        $('#emailCheckArea').text('Email is already taken')
                        break;
                    default:
                        $('#emailCheckArea').text('Email is invalid')
                }
                $('#submitBtn').prop('disabled', true);
                email.removeClass('is-valid');
                email.addClass('is-invalid')
            }
        })
    })

});
