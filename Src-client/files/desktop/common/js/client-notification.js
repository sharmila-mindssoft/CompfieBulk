
function get_notification_count(){
    client_mirror.checkContractExpiration(function (status, data) {
            if (data == null) {
                return
                $(".contract_timer_container").hide()
            }else{
                no_of_days_left = data.no_of_days_left
                $(".contract_timer_container").show()
                if (no_of_days_left <= 30){
                    $(".contract_timer").html(
                        "Contract Expires in "+no_of_days_left+" days"
                    )
                }
                else{
                    // alert("Contract not expired yet"+no_of_days_left)
                }
                notification_count = data.notification_count;
                reminder_count = data.reminder_count;
                escalation_count = data.escalation_count;
                var show_popup = data.show_popup;
                var notification_text = data.notification_text;

                window.localStorage["CLIENT_NOTIFICATION_COUNT"] =  notification_count;
                window.localStorage["CLIENT_REMINDER_COUNT"] = reminder_count;
                window.localStorage["CLIENT_ESCALATION_COUNT"] = escalation_count;

                $("#notification_count").text(window.localStorage["CLIENT_NOTIFICATION_COUNT"]);
                $("#reminder_count").text(window.localStorage["CLIENT_REMINDER_COUNT"]);
                $("#escalation_count").text(window.localStorage["CLIENT_ESCALATION_COUNT"]);

                if(show_popup){
                    console.log(notification_text);
                    showDeletionPopup(notification_text)
                }

            }
        }
    )
}
