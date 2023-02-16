$(document).ready(function(){

    if (localStorage.getItem('created') != null){
        if (localStorage.getItem('created') != 0){
            $(getMessage(localStorage.getItem('created') +' campaigns were created', "success", 'addBulkCustsMsg')).insertAfter('#pagetitle')
            var msg = $('.addBulkCampMsg').children('a').click(() => {
                msg.parent().remove()
            })
            localStorage.removeItem('created')
        } else {
            $(getMessage('No campaigns were created, check your data and try again', "danger", 'addBulkCustsMsg')).insertAfter('#pagetitle')
            var msg = $('.addBulkCampMsg').children('a').click(() => {
                msg.parent().remove()
            })
        }
    }

    $('#campUpload').click(function(){
        var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv)$/;
        if (regex.test($('#campFileUpload').val().toLowerCase())){
            var reader = new FileReader();
            reader.onload = function(e){
                var campArray = [];
                var table = $('<table />');
                table.addClass('table border mb-2')
                var thead = $('<thead />')
                thead.addClass('thead-light')
                var rows = e.target.result.split("\n");
                thead.append('<th>Name</th>').append('<th>Description</th>').append('<th>Template</th>')
                table.append(thead)
                for (var i = 1; i < rows.length; i++) {
                    var row = $("<tr />");
                    var cells = rows[i].split(",");
                    if (cells.length > 1) {
                        for (var j = 0; j < cells.length; j++) {
                            var cell = $("<td />");
                            cell.html(cells[j]);
                            row.append(cell);
                        }
                        var campData = {
                            'name': cells[0],
                            'description': cells[1],
                            'template': cells[2]
                        }
                        campArray.push(campData)
                        table.append(row)
                    }
                }
                $("#csv").html('');
                $("#csv").addClass('px-3 pb-3');
                $("#csv").append(table);
                var importbtn = $('<button />')
                importbtn.addClass('btn btn-primary rounded-lg')
                importbtn.text('Import Campaigns')
                importbtn.on('click', () =>{
                    $.ajax({
                        type: 'POST',
                        url: '/campaigns/bulk',
                        contentType: 'application/json; charset=utf-8',
                        dataType: 'json',
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                        data: JSON.stringify({
                            'campaigns': campArray
                        }),
                        success: function(data){
                            if (data.campaigns.length != 0){
                                localStorage.setItem('created', data.created);
                                $('#campFileUpload').val('');
                                window.location.reload()
                            } else {
                                localStorage.setItem('created', 0);
                                $('#campFileUpload').val('');
                                window.location.reload()
                            }
  
                        }
                    })
                })
                $("#csv").append(importbtn)
            }
            reader.readAsText($('#campFileUpload')[0].files[0])
        } else {
            alert ('Please upload a valid CSV file.')
        }
    })
})

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