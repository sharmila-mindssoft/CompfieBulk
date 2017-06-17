var USER_LE;

function getLegalEntity(LE_ID, LE_NAME) {
    var sEntity = [];
    if (LE_ID != 'all') {
        $.each(USER_LE, function(key, value) {
            if (value.le_id == LE_ID) {
                sEntity.push(value);
            }
        });
    } else {
        var sEntity = USER_LE;
    }

    window.sessionStorage.selectedEntity = JSON.stringify(sEntity, null, ' ');
    window.sessionStorage.selectedEntityName = LE_NAME;
    console.log(LE_NAME);

    var LEIDS = client_mirror.getLEids();
    client_mirror.getNotificationsCount(LEIDS, function(error, response) {
        if (error == null) {
            $.each(response.notification_count, function(k, v) {
                window.sessionStorage.statutory_count = v.statutory_count
                window.sessionStorage.reminder_count = v.reminder_count
                window.sessionStorage.messages_count = v.messages_count
                window.sessionStorage.escalation_count = v.escalation_count
                window.sessionStorage.reminder_expire_count = v.reminder_expire_count
            });
        }
        location.href = '/home';
    });
    
    setTimeout(function () {
        location.href = '/home';
    }, 800);
}

function loadLegalEntityList() {
    var LC = '';
    var LC_COUNT = 1;
    $('.tbody-legal-panel').empty();
    $.each(USER_LE, function(key, value) {
        if (LC != value.c_id) {
            var countrytableRow = $('#act-templates .p-head');
            var clone = countrytableRow.clone();
            $('.acc-title', clone).attr('id', 'heading' + LC_COUNT);
            $('.panel-title a span', clone).text(value.c_name);
            $('.panel-title a', clone).attr('href', '#collapse' + LC_COUNT);
            $('.panel-title a', clone).attr('aria-controls', 'collapse' + LC_COUNT);
            $('.coll-title', clone).attr('id', 'collapse' + LC_COUNT);
            $('.coll-title', clone).attr('aria-labelledb', 'heading' + LC_COUNT);
            $('.tbody-legal-panel').append(clone);
            LC = value.c_id;
            LC_COUNT++;
        }

        var LERow = $('#le-values .table-le-values .row-le-values');
        var clone2 = LERow.clone();
        $('.le_name', clone2).text(value.le_name);
        $(clone2).on('click', function() {
            getLegalEntity(value.le_id, value.le_name);
        });
        $('#collapse' + (LC_COUNT - 1) + ' .tbody-le-list').append(clone2);
    });
}

$(document).ready(function() {
    // if (!client_mirror.verifyLoggedIn())
    //   return;
    console.log("login success");
    USER_LE = client_mirror.getUserLegalEntity();
    loadLegalEntityList();
});
