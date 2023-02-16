$(document).ready(function(){
    
    $('.bi-x').each(function(){
        $(this).on('click', () => {
            var bix = $('.bi-x').index(this)
            var msg = $('.bi-x')
            $(msg[bix]).parent().remove()
        })
    })

    $.ajax({
        type: 'GET',
        url: '/emailservice/check-limit',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            console.log(data)
        }
    })

    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });

})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}

function getUrlId(){
    var url = document.location.href
    var custId = url.split('/')[4]
    return custId
}

function getMessage(text, type, action){
    var message = 
        '<div class="messages">' +
            '<div class="row mx-0 align-items-center ' + action + ' alert alert-sm rounded-sm alert-'+ type +'">' +
                '<div>' + text + '</div>'+
                '<a class="bi bi-x ml-auto"></a>' + 
            '</div>'
        '</div>';
    
    return message
}