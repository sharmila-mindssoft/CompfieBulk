var from_count = 0;
var page_count = 50;
var LEIDS = client_mirror.getLEids();
function loadMessages(data) {
    var isEmpty = true;
    $('.tbody-message-list').find('tr').remove();
    $.each(data, function(k, v) {
        var le_ids = [v.le_id];
        isEmpty = false;
        var tableRow = $('#templates .table-message .table-row');
        var rowClone = tableRow.clone();
        rowClone.on('click', function(e) {
            var row = $(this);
            client_mirror.updateNotificationStatus(le_ids, v.notification_id, true, function(error, response) {
                if (error == null) {
                    var data = response.notification_details;
                    $.each(data, function(k1, v1) {
                        $('.act_name').text(v1.act_name);
                        $('.unit').text(v1.unit);
                        $('.compliance_name').text(v1.compliance_name);
                        $('.due_date').text(v1.due_date);
                        $('.delayed_by').text(v1.delayed_by);
                        $('.assignee_name').text(v1.assignee_name);
                        $('.concurrer_name').text(v1.concurrer_name);
                        $('.approver_name').text(v1.approver_name);
                    });
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                    });
                    row.find('td').css('background-color', '#fcfcfc');
                    e.preventDefault();
                } else {
                    displayMessage(error);
                }
            });
        });
        $('.message-content', rowClone).text(v.notification_text);
        $('.message-time', rowClone).text(v.created_on);
        $('.tbody-message-list').append(rowClone);
    });

    if (isEmpty) {
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-message-list").append(clone);
    }
}

function initialize() {
    client_mirror.getNotifications(LEIDS, 3, 0, 50, function(error, response) {
        if (error == null) {
            data = response.escalations;
            loadMessages(data);
        }
    });
}

$(document).ready(function() {
    initialize();
});
''
