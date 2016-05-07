
var remindersList;
var sno=0;
var notificationDict = [];

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function loadReminders(reminders){
    
    var str='';
    for(var reminder in reminders){
      var readStatus = 'unread';
      var notificationId = reminders[reminder]["notification_id"];
      var notificationText = reminders[reminder]["notification_text"];

      var act = notifications[key]["level_1_statutory"];
      var unit = notifications[key]["unit_name"];
      var unitaddress = notifications[key]["unit_address"];
      var compliance = notifications[key]["compliance_name"];
      var duedate = notifications[key]["due_date"];
      var delayedby = notifications[key]["delayed_days"];
      var assignee = notifications[key]["assignee"];
      var concurrence = notifications[key]["concurrence_person"];
      var approval = notifications[key]["approval_person"];

      notificationDict[notificationId] = [act,unit,unitaddress,compliance,duedate,delayedby,assignee,concurrence,approval];


      if (reminders[reminder]["assignee"] != null){
        var assignee1 = reminders[reminder]["assignee"];
        var assigneesplit = assignee1.split(',');  
      }
      
      if(reminders[reminder]["read_status"]){
        readStatus = '';
      }


      str += '<a href="#popup1" style="text-decoration: none;"> <li class="'+readStatus+'" id="notification'+notificationId+'" onclick="changeStatus('+notificationId+','+reminders[reminder]["read_status"]+')">'+notificationText

      if (reminders[reminder]["assignee"] != null){
        str += "<span style='font-weight:bold'>"+assigneesplit[0]+"</span> </li></a>"
      }
    }
    if(str == '' && sno == 0){
      str += '<li style="text-align:center">'+"No Reminders Found"+"</li>"
    }
   $('#reminderList').append(str);      
}

function changeStatus(notification_id, read_status){
  $('#notification'+notification_id).removeClass( "unread" );
  $("#popup1").show();
  var nId;
  var act = notificationDict[notification_id][0];
  var unit = notificationDict[notification_id][1];
  var unitaddress = notificationDict[notification_id][2];
  var compliance = notificationDict[notification_id][3];
  var duedate = notificationDict[notification_id][4];
  var delayedby = notificationDict[notification_id][5];
  var assignee = notificationDict[notification_id][6];
  var concurrence = notificationDict[notification_id][7];
  var approval = notificationDict[notification_id][8];


  var assigneeName;
  var assigneeDetails;
  var concurrenceName;
  var concurrenceDetails;
  var assigneeName;
  var assigneeDetails;

  if(assignee != ''){
    assigneeName = assignee.split(',')[0];
    assigneeDetails = assignee.substring(assignee.indexOf(",")+1).trim().replace(/--, /gi,'');
  }

  if(concurrence != '' && concurrence != null){
    concurrenceName = concurrence.split(',')[0];
    concurrenceDetails = concurrence.substring(concurrence.indexOf(",")+1).trim().replace(/--, /gi,'');
  }else{
    concurrenceName = '-'
    concurrenceDetails = '-' 
  }

  if(approval != ''){
    approvalName = approval.split(',')[0];
    approvalDetails = approval.substring(approval.indexOf(",")+1).trim().replace(/--, /gi,'');
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

function get_reminders(sno){
  displayLoader();
  function onSuccess(data){
    remindersList = data['notifications'];
    loadReminders(remindersList);
    if(remindersList.length == 0){
        $('#pagination').hide();
    }else{
        $('#pagination').show();
    }
    hideLoader();
  }
  function onFailure(error){
        console.log(error);
        hideLoader();
  }
  client_mirror.getNotifications( 'Reminder', sno,
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

$('#pagination').click(function(){
    get_notifications(sno);
});

function initialize(){
  sno = 0;
  notificationDict = [];
  $("#reminderList").empty();
  get_reminders(sno);
  /*setInterval(function() {
      get_reminders();
  }, 10000);*/
  
}

$(function() {
  initialize();
});