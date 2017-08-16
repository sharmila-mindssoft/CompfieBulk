var MessageList;
var from_count = 0;
var page_count = 50;

function updateNotificationStatus(m_id, r_status) {
    displayLoader();
    mirror.updateMessageStatus(m_id, r_status, function(error, response) {
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
    $.each(MessageList, function(k, v) {
        isEmpty = false;
        var tableRow = $('#templates .table-message .table-row');
        var rowClone = tableRow.clone();

        rowClone.on('click', function(e) {
            updateNotificationStatus(v.message_id, true);
            e.preventDefault();
        });

        $('.message-content', rowClone).text(v.message_heading + ' - ' + v.message_text);
        $('.message-time', rowClone).text(v.created_on);
        $('.message-user', rowClone).text('User: ' + v.created_by);
        $('.tbody-message-list').append(rowClone);
    });

    if (isEmpty) {
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-message-list").append(clone);
        $('.message-menu').find('.notify-icon-container').hide();
    }else{
        $('.message-menu').find('.notify-icon-container').show();
    }
    hideLoader();
}

// page load
function initialize() {
    displayLoader();
    mirror.getMessages(from_count, page_count, function(error, response) {
        if (error != null) {
            displayMessage(error);
            hideLoader();
        } else {
            MessageList = response.messages;
            loadMessages();
        
        }
    });
}

$(document).ready(function() {
    initialize();
});
