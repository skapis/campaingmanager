$(document).ready(function(){
    

    $('#editCust').click(function(){
        var firstName = $('[name="firstName"]');
        var lastName = $('[name="lastName"]');
        var email = $('[name="email"]');
        var gender = $('[name="gender"]');
        var age = $('[name="age"]');
        var birthDate = $('[name="birthDate"]');

        firstName.prop('disabled', false);
        lastName.prop('disabled', false);
        email.prop('disabled', false);
        gender.prop('disabled', false);
        age.prop('disabled', false);
        birthDate.prop('disabled', false);

        $('.actions').hide() // remove buttons for edit and delete, when user edits customer data
        $('.edit').show(); 
        var submit = $('<button/>')
            .text('Save')
            .addClass('btn btn-primary rounded-lg mr-2')
            .on('click', () => {
                $.ajax({
                    type: 'POST',
                    url: '/customer/'+ getUrlId(),
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    data: JSON.stringify({
                        'firstName': firstName.val(),
                        'lastName': lastName.val(),
                        'email': email.val(),
                        'gender': gender.val(),
                        'age': age.val(),
                        'birthDate': birthDate.val()

                    }),
                    success: function(data){
                        firstName.val(data.firstName).prop('disabled', true)
                        lastName.val(data.lastName).prop('disabled', true)
                        email.val(data.email).prop('disabled', true)
                        gender.val(data.gender).change().prop('disabled', true)
                        age.val(data.age).prop('disabled', true)
                        birthDate.val(data.birthDate).prop('disabled', true)

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
                firstName.prop('disabled', true);
                lastName.prop('disabled', true);
                email.prop('disabled', true);
                gender.prop('disabled', true);
                age.prop('disabled', true);
                birthDate.prop('disabled', true);
                $('.edit').hide();
                $('.actions').show()
            })
            ;
        if (!$('#cancel').length){
            $('.edit').append(submit);
            $('.edit').append(cancel);
        }

    });

    $('.removeCamp').each(function(){
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

    $('#addCampBtn').click(function(){
        $.ajax({
            type: 'GET',
            url: '/customer/available-camps?custId='+ getUrlId(),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data){
                var campList = $('#custCampList')
                campList.empty()
                if (data.length != 0){
                    data.map((item) => {
                        var li = 
                            '<li class="list-group-item border-0">' +
                                '<div class="form-check checkbox-lg">' +
                                    '<input class="form-check-input" type="checkbox" value="'+ item.campaignId +'" name="camps" style="transform: scale(1.25);">' +
                                    '<label class="form-check-label">'+ item.name +'</label>' +
                                '</div>' +
                            '</li>'
                        campList.append(li)    
                    })
                } else {
                    var nocampli = '<li class="list-group-item border-0 font-weight-bold">No available campaign to add</li>'
                    campList.append(nocampli)
                    campList.removeClass('border')
                }
                

            }
        })
    })

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