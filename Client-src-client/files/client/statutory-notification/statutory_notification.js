var from_count = 0;
var page_count = 50;
var LEIDS = client_mirror.getLEids();
function loadMessages(data) {
    var isEmpty = true;
    $('.tbody-message-list').find('tr').remove();
    $.each(data, function(k, v) {
        isEmpty = false;
        var tableRow = $('#templates .table-message .table-row');
        var rowClone = tableRow.clone();
        rowClone.on('click', function(e) {
            var row = $(this);
            client_mirror.updateStatutoryNotificationsStatus(LEIDS, v.notification_id, true, function(error, response) {
                if (error == null) {
                    var data_new = response.statutory_notification_details;
                    $.each(data_new, function(k1, v1) {
                        $('.popup-statutory').text(v1.statutory_provision);
                        $('.popup-compliancetask').text(v1.compliance_task);
                        $('.popup-description').text(v1.compliance_description);
                        $('.popup-penalconse').text(v1.penal_consequences);
                        $('.popup-frequency').text(v1.freq_name);
                        $('.popup-occurance').text(v1.summary);
                        $('.popup-referencelink a span').text(v1.refer);
                        $('.popup-referencelink a').attr('href', v1.reference_link);
                    });
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                        close: function () {
                            initialize();
                        }
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
        $('.message-user', rowClone).text(v.user_name);
        $('.tbody-message-list').append(rowClone);
        return k<50;
    });
    
    if (isEmpty) {
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-message-list").append(clone);
    }
}

function initialize() {
    displayLoader();
    client_mirror.getStatutoryNotifications(LEIDS, 0, 50, function(error, response) {
        if (error == null) {
            data = response.statutory;
            statutory_count = response.statutory_count;
            if(statutory_count == 0) {
                window.sessionStorage.statutory_count = 0;
                $('.notification-menu').find('.notify-icon-container').hide();
            }
            loadMessages(data);
        }
        hideLoader();
    });
}

$(document).ready(function() {
    initialize();
});
''
