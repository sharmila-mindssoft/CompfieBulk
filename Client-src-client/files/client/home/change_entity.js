function get_notification_count() {
    var LEIDS = client_mirror.getLEids();
    client_mirror.getNotificationsCount(LEIDS, function(error, response) {
        if (error == null) {
            $.each(response.notification_count, function(k, v) {
                window.localStorage.statutory_count = v.statutory_count
                window.localStorage.reminder_count = v.reminder_count
                window.localStorage.messages_count = v.messages_count
                window.localStorage.escalation_count = v.escalation_count
            });
        }
    });
}

function getLegalEntityChange(LE_ID, LE_NAME) {
    var sEntity = [];
    var USER_LE = client_mirror.getUserLegalEntity();
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
    get_notification_count();
    location.reload(window.sessionStorage.selectedEntity);
}

function loadLegalEntityListChange() {
    var LC = '';
    var LC_COUNT = 1;
    var USER_LE = client_mirror.getUserLegalEntity();
    $('.tbody-legal-panel-change').empty();
    $.each(USER_LE, function(key, value) {
        if (LC != value.c_id) {
            var countrytableRow = $('#le-templates-change .p-head');
            var clone = countrytableRow.clone();
            $('.acc-title', clone).attr('id', 'heading' + LC_COUNT);
            $('.panel-title a span', clone).text(value.c_name);
            $('.panel-title a', clone).attr('href', '#collapse' + LC_COUNT);
            $('.panel-title a', clone).attr('aria-controls', 'collapse' + LC_COUNT);
            $('.coll-title', clone).attr('id', 'collapse' + LC_COUNT);
            $('.coll-title', clone).attr('aria-labelledb', 'heading' + LC_COUNT);
            $('.tbody-legal-panel-change').append(clone);
            LC = value.c_id;
            LC_COUNT++;
        }
        var LERow = $('#le-values-change .table-le-values .row-le-values');
        var clone2 = LERow.clone();
        $('.le_name', clone2).text(value.le_name);
        $(clone2).on('click', function() {
            getLegalEntityChange(value.le_id, value.le_name);
        });
        $('#collapse' + (LC_COUNT - 1) + ' .tbody-le-list-change').append(clone2);
    });
}
