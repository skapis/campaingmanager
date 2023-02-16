$(document).ready(function(){
    
    $('#editCamp').click(function(){
        var name = $('[name="name"]');
        var description = $('[name="description"]');
        var template = $('[name="template"]');

        name.prop('disabled', false);
        description.prop('disabled', false);
        template.prop('disabled', false);

        $('.actions').hide() // remove buttons for edit and delete, when user edits campaign data
        $('.edit').show(); 
        var submit = $('<button/>')
            .text('Save')
            .addClass('btn btn-primary rounded-lg mr-2')
            .on('click', () => {
                $.ajax({
                    type: 'POST',
                    url: '/campaign/'+ getUrlId(),
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    data: JSON.stringify({
                        'name': name.val(),
                        'description': description.val(),
                        'template': template.val(),
                    }),
                    success: function(data){
                        name.val(data.name).prop('disabled', true)
                        description.val(data.description).prop('disabled', true)
                        template.val(data.template).prop('disabled', true)
                        

                        $('.edit').hide();
                        $('.actions').show();
                            $('.editMsg').remove()
                            $(getMessage("Changes were saved", "success", 'editMsg')).insertAfter('#pagetitle')
                            var editMsg = $('.editMsg').children('a').click(() => {
                                editMsg.parent().remove()
                            })

                    }
                })
            });
        var cancel = $('<button/>')
            .text('Cancel')
            .addClass('btn btn-danger rounded-lg')
            .attr('id', 'cancel')
            .on('click', () => {
                name.prop('disabled', true);
                description.prop('disabled', true);
                template.prop('disabled', true);
                $('.edit').hide();
                $('.actions').show()
            })
            ;
        if (!$('#cancel').length){
            $('.edit').append(submit);
            $('.edit').append(cancel);
        }

    });

    $('#changeCampState').click(function(){
        $.ajax({
            type: 'POST',
                url: '/campaign/change-state',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                data: JSON.stringify({
                    'campId': getUrlId()
                }),
                success: function(data){
                    if (data.state == true){
                        $('#changeCampState')
                            .text('Disable Campaign')
                            .removeClass('btn-success')
                            .addClass('btn-secondary')
                        $('.stateMsg').remove()
                        $(getMessage('The campaign is now enabled, you can send emails to customers', "success", 'stateMsg'))
                            .insertAfter('#pagetitle')
                        var msg = $('.stateMsg').children('a').click(() => {
                            msg.parent().remove()
                        })
                        $('#sendMails').prop('disabled', false)
                    } else {
                        $('#changeCampState')
                        .text('Enable Campaign')
                        .removeClass('btn-secondary')
                        .addClass('btn-success')
                        $('.stateMsg').remove()
                        $(getMessage('This campaign is not enabled, you cannot send emails, until you enable it.', "danger", 'stateMsg'))
                            .insertAfter('#pagetitle')
                        var msg = $('.stateMsg').children('a').click(() => {
                            msg.parent().remove()
                        })
                        $('#sendMails').prop('disabled', true)
                    }    
                }
        })
    })

    $('.removeCust').each(function(){
        $(this).on('click', () => {
            $.ajax({
                type: 'POST',
                url: '/remove-camp-cust',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                data: JSON.stringify({
                    'ccId': $(this).attr('id')

                }),
                success: function(data){
                    $('#'+data.id).parent().parent().remove()
                    $('.removeCampMsg').remove()
                    $(getMessage(data.message, "success", 'removeCampMsg')).insertAfter('#pagetitle')
                    var editMsg = $('.removeCampMsg').children('a').click(() => {
                        editMsg.parent().remove()
                    })
                }
            })
        })
    })

    $('#addCustsBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/campaign/available-custs?campId='+ getUrlId(),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                var custList = $('#campCustList')
                custList.empty()
                if (data.length != 0){
                    data.map((item) => {
                        var li = 
                            '<li class="list-group-item border-0">' +
                                '<div class="form-check checkbox-lg">' +
                                    '<input class="form-check-input" type="checkbox" value="'+ item.customerId +'" name="custs" style="transform: scale(1.25);">' +
                                    '<label class="form-check-label">'+item.first_name + ' ' + item.last_name +' ('+ item.email +')</label>' +
                                '</div>' +
                            '</li>'
                        custList.append(li)    
                    })
                } else {
                    var nocampli = '<li class="list-group-item border-0 font-weight-bold">No available customers to add</li>'
                    custList.append(nocampli)
                    custList.removeClass('border')
                }
            }
        })
    });

})

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