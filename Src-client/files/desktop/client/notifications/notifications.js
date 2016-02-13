var notificationsList;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function loadNotifications(notifications){
    $("#notificationsList").empty();
    var str='';
    $.each(notifications, function(key, value){
        var readStatus = 'unread';
        var notificationId = notifications[key]["notification_id"];
        var notificationText = notifications[key]["notification_text"];
        var extraDetails = notifications[key]["extra_details"];
        var updatedon = notifications[key]["updated_on"];
        
        if(notifications[key]["read_status"]){
            readStatus = '';
        }
        str += '<li class="'+readStatus+'" onclick="changeStatus('+notificationId+','+notifications[key]["read_status"]+')"><a href="#popup1" style="text-decoration: none;"> '+notificationText+'<p class="subtext"><span class="time">'+updatedon+'</span><span class="notification-cat">Category: '+extraDetails+'</span></p> </a></li>';
    });
    $('#notificationsList').append(str);      
}

function changeStatus(notification_id, read_status){
    $("#popup1").show();
    var nId;
    var act;
    var unit;
    var compliance;
    var duedate;
    var delayedby;
    var assignee;
    var concurrence;
    var approval;
    var notifications = notificationsList;
    $.each(notifications, function(i, value) {
        nId = notifications[i]["notification_id"];
        if(nId == notification_id){
            act = notifications[i]["level_1_statutory"];
            unit = notifications[i]["unit_name"];
            unitaddress = notifications[i]["unit_address"];
            compliance = notifications[i]["compliance_name"];
            duedate = notifications[i]["due_date"];
            delayedby = notifications[i]["delayed_days"];
            assignee = notifications[i]["assignee"];
            concurrence = notifications[i]["concurrence_person"];
            approval = notifications[i]["approval_person"];            
        }
    });

    var assigneeName;
    var assigneeDetails;
    var concurrenceName;
    var concurrenceDetails;
    var assigneeName;
    var assigneeDetails;

    if(assignee != ''){
        assigneeName = assignee.split(',')[0];
        assigneeDetails = assignee.substring(assignee.indexOf(",")+1).trim();
    }

    if(concurrence != ''){
        concurrenceName = concurrence.split(',')[0];
        concurrenceDetails = concurrence.substring(concurrence.indexOf(",")+1).trim();
    }

    if(approval != ''){
        approvalName = approval.split(',')[0];
        approvalDetails = approval.substring(approval.indexOf(",")+1).trim();
    }

    $(".popup_act").text(act);
    $(".popup_unit").html('<abbr class="page-load tipso_style" title="'+ unitaddress +'"></abbr>'+unit);
    $(".popup_compliance").text(compliance);
    $(".popup_duedate").text(duedate);
    $(".popup_delayedby").text(delayedby);
    $(".popup_assignee").html(assigneeName +'<br>'+ assigneeDetails);
    $(".popup_concurrence").html(concurrenceName +'<br>'+ concurrenceDetails);
    $(".popup_approval").html(approvalName +'<br>'+ approvalDetails);

    if(read_status == false){
        function onSuccess(response){
        
        }
        function onFailure(error) {
            displayMessage = error
        }
        client_mirror.updateNotificationStatus(parseInt(notification_id), true,
            function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
               onFailure(error);
            }
        });
    }
}


function initialize(){
    function onSuccess(data){
        notificationsList = data['notifications'];
        loadNotifications(notificationsList)
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getNotifications( 'Notification',
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }

    );
}

$(function() {
    initialize();
});