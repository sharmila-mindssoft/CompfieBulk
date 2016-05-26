
var escalationsList;
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

function loadEscalations(escalations){
    
    var str='';
    for(var reminder in escalations){
      sno++;
      var readStatus = 'unread';
      var notificationId = escalations[reminder]["notification_id"];
      var notificationText = escalations[reminder]["notification_text"];
      var assignee = escalations[reminder]["assignee"];
      var assigneesplit = assignee.split(',');
      var act = escalations[reminder]["level_1_statutory"];
      var unit = escalations[reminder]["unit_name"];
      var unitaddress = escalations[reminder]["unit_address"];
      var compliance = escalations[reminder]["compliance_name"];
      var duedate = escalations[reminder]["due_date"];
      var delayedby = escalations[reminder]["delayed_days"];
     
      notificationDict[notificationId] = [act,unit,unitaddress,compliance,duedate,delayedby];

      if(escalations[reminder]["read_status"]){
        readStatus = '';
      }

      if(assignee != null){
        str += '<a href="#popup1" style="text-decoration: none;"> <li id="notification'+notificationId+
        '" class="'+readStatus+'" onclick="changeStatus('+notificationId+','+escalations[reminder]["read_status"]+
        ')"> <p style="width:90%;text-align:left">'+notificationText+
        "</p> <span style='font-weight:bold;vertical-align:bottom'>"+assigneesplit[0]+
        " <abbr class='page-load' title='"+assigneesplit[0]+
        "'> <img src='images/icon-info-blue.png' style='width:15px;height:15px'> </abbr></span> </li></a>"
      }else{
        str += '<li id="notification'+notificationId+
        '" class="'+readStatus+'" onclick="changeStatus('+notificationId+','+escalations[reminder]["read_status"]+
        ')"> <p style="width:90%;text-align:left">'+notificationText+
        "</p> <span style='font-weight:bold;vertical-align:bottom'>"+assigneesplit[0]+
        " <abbr class='page-load' title='"+assigneesplit[0]+
        "'> <img src='images/icon-info-blue.png' style='width:15px;height:15px'> </abbr></span> </li>"
      }
    }

    if(str == '' && sno == 0){
      str += '<li style="text-align:center">'+"No Escalations Found"+"</li>"
    }
   $('#escalationList').append(str);      
}

function changeStatus(notification_id, read_status){
  $('#notification'+notification_id).removeClass( "unread" );
  $("#popup1").show();
  var act = notificationDict[notification_id][0];
  var unit = notificationDict[notification_id][1];
  var unitaddress = notificationDict[notification_id][2];
  var compliance = notificationDict[notification_id][3];
  var duedate = notificationDict[notification_id][4];
  var delayedby = notificationDict[notification_id][5];

  $(".popup_act").text(act);
  $(".popup_unit").html('<abbr class="page-load tipso_style" title="'+ unitaddress +'"></abbr>'+unit);
  $(".popup_compliance").text(compliance);
  $(".popup_duedate").text(duedate);
  $(".popup_delayedby").text(delayedby);
  
  if(read_status == false){
    function onSuccess(response){
      get_notification_count();
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

function get_escalations(sno){
  displayLoader();
    function onSuccess(data){
    escalationsList = data['notifications'];
    loadEscalations(escalationsList);
    if(escalationsList.length == 0){
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
  client_mirror.getNotifications( 'Escalation', sno, 
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
  $("#escalationList").empty();
  sno = 0;
  notificationDict = [];
  get_escalations(sno);
  /*setInterval(function() {
      get_escalations();
  }, 10000);*/
  
}

$(function() {
  initialize();
});