var NotificationList;
var from_count = 0;
var page_count = 50;

function updateNotificationStatus(n_id, u_id, r_status) {
    displayLoader();
    mirror.updateStatutoryNotificationStatus(n_id, u_id, r_status, function(error, response) {
        if (error == null) {
            window.sessionStorage.statutory_count = response.s_count;
            window.sessionStorage.messages_count = response.m_count;
            initialize();
        } else {
            displayMessage(error);
            hideLoader();
        }

    });
}
// User List render process
function loadMessages() {
    var isEmpty = true;
    $('.tbody-message-list').find('tr').remove();
    $.each(NotificationList, function(k, v) {
        isEmpty = false;
        var tableRow = $('#templates .table-message .table-row');
        var rowClone = tableRow.clone();

        rowClone.on('click', function(e) {
            mirror.getComplianceInfo(v.compliance_id, function(error, response) {
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
            });
        });

        $('.message-content', rowClone).text(v.notification_text);
        $('.message-time', rowClone).text(v.created_on);
        $('.message-user', rowClone).text('User: ' + v.created_by);
        $('.tbody-message-list').append(rowClone);
    });

    if (isEmpty) {
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-message-list").append(clone);
        $('.notification-menu').find('.notify-icon-container').hide();
    }else{
        $('.notification-menu').find('.notify-icon-container').show();
    }

    hideLoader();
}

// page load
function initialize() {
    displayLoader();
    mirror.getStatutoryNotifications(from_count, page_count, function(error, response) {
        if (error != null) {
            displayMessage(error);
            hideLoader();
        } else {
            NotificationList = response.statutory_notifications;
            loadMessages();
        }
    });
}

$(document).ready(function() {
    initialize();
});
