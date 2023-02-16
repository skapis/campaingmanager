$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/customer/available-camps?custId='+ getCustId(),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            console.log(data)
        }
    })
})