
var escalationsList;
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function loadEscalations(escalations){
    $("#reminderList").empty();
    var str='';
    for(var reminder in escalations){
      var readStatus = 'unread';
      var notificationId = escalations[reminder]["notification_id"];
      var notificationText = escalations[reminder]["notification_text"];

      var assignee = escalations[reminder]["assignee"];
      var assigneesplit = assignee.split(',');

      if(escalations[reminder]["read_status"]){
        readStatus = '';
      }

      str += '<a href="#popup1" style="text-decoration: none;"> <li class="'+readStatus+'" onclick="changeStatus('+notificationId+','+escalations[reminder]["read_status"]+')">'+notificationText+" <span style='font-weight:bold'>"+assigneesplit[0]+" <abbr class='page-load' title='"+assigneesplit[0]+"'> <img src='images/icon-info-blue.png'  style='width:15px;height:15px'> </abbr></span> </li></a>"
    }
   $('#reminderList').append(str);      
}

function changeStatus(notification_id, read_status){

  $("#popup1").show();
  var nId;
  var act;
  var unit;
  var compliance;
  var duedate;
  var delayedby;
  var escalations = escalationsList;
  for(var i in escalations){
    nId = escalations[i]["notification_id"];
    if(nId == notification_id){
      act = escalations[i]["level_1_statutory"];
      unit = escalations[i]["unit_name"];
      unitaddress = escalations[i]["unit_address"];
      compliance = escalations[i]["compliance_name"];
      duedate = escalations[i]["due_date"];
      delayedby = escalations[i]["delayed_days"];
      break;
    }
  }
  $(".popup_act").text(act);
  $(".popup_unit").html('<abbr class="page-load tipso_style" title="'+ unitaddress +'"></abbr>'+unit);
  $(".popup_compliance").text(compliance);
  $(".popup_duedate").text(duedate);
  $(".popup_delayedby").text(delayedby);
  
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
    escalationsList = data['notifications'];
    loadEscalations(escalationsList)
  }
  function onFailure(error){
        console.log(error);
  }
  client_mirror.getNotifications( 'Escalation',
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