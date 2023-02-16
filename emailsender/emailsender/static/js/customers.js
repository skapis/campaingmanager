$(document).ready(function(){

    if (localStorage.getItem('created') != null){
        if (localStorage.getItem('created') != 0){
            $(getMessage(localStorage.getItem('created') +' customers were created', "success", 'addBulkCustsMsg')).insertAfter('#pagetitle')
            var msg = $('.addBulkCustsMsg').children('a').click(() => {
                msg.parent().remove()
            })
            localStorage.removeItem('created')
        } else {
            $(getMessage('No customers were created, check your data and try again', "danger", 'addBulkCustsMsg')).insertAfter('#pagetitle')
            var msg = $('.addBulkCustsMsg').children('a').click(() => {
                msg.parent().remove()
            })
        }
    }

    $('#custUpload').click(function(){
        var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv)$/;
        if (regex.test($('#custFileUpload').val().toLowerCase())){
            var reader = new FileReader();
            reader.onload = function(e){
                var custArray = [];
                var table = $('<table />');
                table.addClass('table border mb-2')
                var thead = $('<thead />')
                thead.addClass('thead-light')
                var rows = e.target.result.split("\n");
                thead
                    .append('<th>First Name</th>')
                    .append('<th>Last Name</th>')
                    .append('<th>Email</th>')
                    .append('<th>Gender</th>')
                    .append('<th>Age</th>')
                    .append('<th>Birth Date</th>')
                    .append('<th>Campaign</th>')
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
                        var custData = {
                            'firstName': cells[0],
                            'lastName': cells[1],
                            'email': cells[2],
                            'gender': cells[3],
                            'age': cells[4],
                            'birthdate': cells[5],
                            'campaign': cells[6]
                        }
                        custArray.push(custData)
                        table.append(row)
                    }
                }
                $("#csv").html('');
                $("#csv").addClass('px-3 pb-3');
                $("#csv").append(table);
                var importbtn = $('<button />')
                importbtn.addClass('btn btn-primary rounded-lg')
                importbtn.text('Import Customers')
                importbtn.on('click', () =>{
                    $.ajax({
                        type: 'POST',
                        url: '/customers/bulk',
                        contentType: 'application/json; charset=utf-8',
                        dataType: 'json',
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": getCookie("csrftoken"),
                        },
                        data: JSON.stringify({
                            'customers': custArray
                        }),
                        success: function(data){
                            if (data.customers.length != 0){
                                localStorage.setItem('created', data.created)
                                $('#custFileUpload').val('')
                                window.location.reload()

                            } else {
                                localStorage.setItem('created', 0)
                                $('#custFileUpload').val('')
                                window.location.reload()
                            }
                        }
                    })
                })
                $("#csv").append(importbtn)
            }
            reader.readAsText($('#custFileUpload')[0].files[0])
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
