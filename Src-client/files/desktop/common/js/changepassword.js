function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$("#submit").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val();
  var newpassword = $("#newpassword").val();
  var confirmpassword = $("#confirmpassword").val();
  if(currentpassword == '') {
    displayMessage("Current Password Required");
  } else if(newpassword == '') {
    displayMessage("New Password Required");
  } else if(confirmpassword == '') {
    displayMessage("Confirm Password Required");
  } else if(confirmpassword != newpassword) {
    displayMessage("New Password & Confirm Password is Not Match");
  } else {
      function onSuccess(data){
          displayMessage("Password Changed Successfully");
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
      }
      function onFailure(error){
      }
      mirror.changePassword(currentpassword, newpassword, 
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
    );
    }
  });