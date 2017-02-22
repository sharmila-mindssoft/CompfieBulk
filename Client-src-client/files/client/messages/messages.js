var from_count = 0;
var page_count = 50;

function loadMessages(data) {
    var isEmpty = true;
    $('.tbody-message-list').find('tr').remove();
    $.each(data, function(k, v) {
        isEmpty = false;
        var tableRow = $('#templates .table-message .table-row');
        var rowClone = tableRow.clone();

        rowClone.on('click', function(e) {
            /*mirror.updateNotificationStatus(le_id, v.compliance_id, 1 function(error, response) {
                if (error == null) {
                    $('.popup-statutory').text(response.s_pro);
                    $('.popup-compliancetask').text(response.c_task);
                    $('.popup-description').text(response.descrip);
                    $('.popup-penalconse').text(response.p_cons);
                    $('.popup-frequency').text(response.freq);
                    $('.popup-occurance').text(response.summary);
                    $('.popup-applicablelocation').text(response.locat);
                    $('.popup-referencelink a span').text(response.refer);
                    $('.popup-referencelink a').attr('href', response.refer);
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                    });
                    updateNotificationStatus(v.notification_id, v.user_id, true);
                    e.preventDefault();
                } else {
                    displayMessage(error);
                }
            });*/
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
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
    client_mirror.getNotifications(LEIDS, 4, 0, 50, function(error, response) {
        if (error == null) {
            data = response.messages;
            loadMessages(data);
        }
    });
}

$(document).ready(function() {
    initialize();
});
