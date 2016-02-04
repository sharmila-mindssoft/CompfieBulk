
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
    var readStatus = '';
    var notificationId = 0;
    if( readStatus = 'unread'){
      readStatus = 'unread';
    }
    str += '<li class="'+readStatus+'" onclick="changeStatus('+notificationId+')">'+readStatus+"<span>"+readStatus+"</span> </li>"
    }
   $('#reminderList').append(str);      
}

function changeStatus(notification_id){

    function onSuccess(response){
        
      }
    function onFailure(error) {
        displayMessage = error
    }
    client_mirror.updateNotificationStatus(parseInt(notification_id), "read",
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      });
}


function initialize(){

  function onSuccess(data){
    var reminders = data['profile_detail'];
    loadReminders(reminders)
  }
  function onFailure(error){
        console.log(error);
  }
  client_mirror.getNotifications( 'Reminder',
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