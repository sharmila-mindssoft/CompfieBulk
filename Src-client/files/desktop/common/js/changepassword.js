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
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage("Current Password Required");
  } else if(newpassword.length == 0) {
    displayMessage("New Password Required");
  } else if(confirmpassword.length == 0) {
    displayMessage("Confirm Password Required");
  } else if(confirmpassword != newpassword) {
    displayMessage("New Password & Confirm Password Do Not Match");
  } else {
      function onSuccess(data){
          displayMessage("Password Changed Successfully");
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
      }
      function onFailure(error){
        if(error == "InvalidCurrentPassword"){
          displayMessage("Invalid Current Password");
        }
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

$("#submit-client").click(function(){
  displayMessage("");
  var currentpassword = $("#currentpassword").val().trim();
  var newpassword = $("#newpassword").val().trim();
  var confirmpassword = $("#confirmpassword").val().trim();
  if(currentpassword.length == 0) {
    displayMessage("Current Password Required");
  } else if(newpassword.length == 0) {
    displayMessage("New Password Required");
  } else if(confirmpassword.length == 0) {
    displayMessage("Confirm Password Required");
  } else if(confirmpassword != newpassword) {
    displayMessage("New Password & Confirm Password Do Not Match");
  } else {
      function onSuccess(data){
          console.log("inside onsucces in change password")
          displayMessage("Password Changed Successfully");
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
      }
      function onFailure(error){
        console.log("inside onFailure in change password")
        if(error == "InvalidCurrentPassword"){
          displayMessage("Invalid Current Password");
        }
      }
      client_mirror.changePassword(currentpassword, newpassword, 
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
$(document).ready(function(){
  $("#currentpassword").focus();
});