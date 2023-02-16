$(document).ready(function(){

    $('#editTemplate').click(function(){
        var name = $('[name="name"]');
        var header = $('[name="header"]');
        var content = $('[name="content"]');
        var subject = $('[name="subject"]');

        name.prop('disabled', false);
        header.prop('disabled', false);
        content.prop('disabled', false);
        subject.prop('disabled', false);

        $('.actions').hide() // remove buttons for edit and delete, when user edits customer data
        $('.edit').show(); 
        var submit = $('<button/>')
            .text('Save')
            .addClass('btn btn-primary rounded-lg mr-2')
            .on('click', () => {
                $.ajax({
                    type: 'POST',
                    url: '/emailservice/template/'+ getTemplateId(),
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    data: JSON.stringify({
                        'name': name.val(),
                        'subject': subject.val(),
                        'header': header.val(),
                        'content': content.val(),

                    }),
                    success: function(data){
                        name.val(data.name).prop('disabled', true)
                        subject.val(data.subject).prop('disabled', true)
                        header.val(data.header).prop('disabled', true)
                        content.val(data.content).change().prop('disabled', true)

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
                subject.prop('disabled', true);
                header.prop('disabled', true);
                content.prop('disabled', true);
                $('.edit').hide();
                $('.actions').show()
            })
            ;
        if (!$('#cancel').length){
            $('.edit').append(submit);
            $('.edit').append(cancel);
        }

    });


})

function getTemplateId(){
    var url = document.location.href
    var templateId = url.split('/')[5]
    return templateId
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