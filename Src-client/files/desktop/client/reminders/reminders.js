
var remindersList;
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function loadReminders(reminders){
    $("#reminderList").empty();
    var str='';
    for(var reminder in reminders){
      var readStatus = 'unread';
      var notificationId = reminders[reminder]["notification_id"];
      var notificationText = reminders[reminder]["notification_text"];

      if (reminders[reminder]["assignee"] != null){
        var assignee = reminders[reminder]["assignee"];
        var assigneesplit = assignee.split(',');  
      }
      

      if(reminders[reminder]["read_status"]){
        readStatus = '';
      }


      str += '<a href="#popup1" style="text-decoration: none;"> <li class="'+readStatus+'" id="notification'+notificationId+'" onclick="changeStatus('+notificationId+','+reminders[reminder]["read_status"]+')">'+notificationText

      if (reminders[reminder]["assignee"] != null){
        str += "<span style='font-weight:bold'>"+assigneesplit[0]+"</span> </li></a>"
      }
    }
    if(str == ''){
      str += '<li style="text-align:center">'+"No Reminders Found"+"</li>"
    }
   $('#reminderList').append(str);      
}

function changeStatus(notification_id, read_status){
  $('#notification'+notification_id).removeClass( "unread" );
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
  var reminders = remindersList;
  for(var i in reminders){
    nId = reminders[i]["notification_id"];
    if(nId == notification_id){
      act = reminders[i]["level_1_statutory"];
      unit = reminders[i]["unit_name"];
      unitaddress = reminders[i]["unit_address"];
      compliance = reminders[i]["compliance_name"];
      duedate = reminders[i]["due_date"];
      delayedby = reminders[i]["delayed_days"];
      assignee = reminders[i]["assignee"];
      concurrence = reminders[i]["concurrence_person"];
      approval = reminders[i]["approval_person"];
      break;
    }
  }

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

function get_reminders(){
  function onSuccess(data){
    remindersList = data['notifications'];
    loadReminders(remindersList)
  }
  function onFailure(error){
        console.log(error);
  }
  client_mirror.getNotifications( 'Reminder', 0, 
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

function initialize(){
  get_reminders();
  setInterval(function() {
      get_reminders();
  }, 10000);
  
}

$(function() {
  initialize();
});