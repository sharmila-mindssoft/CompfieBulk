$(function() {
    $("#from-date").datepicker({
        showButtonPanel: true,
        closeText: 'Clear',
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ],
        maxDate: new Date(),
        onClose: function(selectedDate) {
            $("#to-date").datepicker("option", "minDate", selectedDate);
            var event = arguments.callee.caller.caller.arguments[0];
            if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
                $(this).val('');
            }
        }
    });
    $("#to-date").datepicker({
        showButtonPanel: true,
        closeText: 'Clear',
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ],
        maxDate: new Date(),
        onClose: function(selectedDate) {
                var event = arguments.callee.caller.caller.arguments[0];
                if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
                    $(this).val('');
                }
            }
    });
});