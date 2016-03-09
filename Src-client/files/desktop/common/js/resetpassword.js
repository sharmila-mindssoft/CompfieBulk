function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}
$("#submit").click(function(){
    $(".error-message").html("");
    var resetToken = "a7da78729ce049d8b29f2520c8c57496";
    var newpassword = $("#newpassword").val().trim();
    var confirmpassword = $("#confirmpassword").val().trim();

    if(newpassword.length == 0) {
      $(".error-message").html("New Password Required");
    } else if(confirmpassword.length == 0) {
      $(".error-message").html("Confirm Password Required");
    } else if(confirmpassword != newpassword) {
      $(".error-message").html("New Password & Confirm Password is Not Match");
    } else {

        function onSuccess(data){
          displayMessage("Password Reset Successfully");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
        }
        function onFailure(error){
          if(error == "InvalidResetToken"){
            displayMessage("Invalid Reset Token");
          }
        }
        mirror.resetPassword(resetToken, newpassword, 
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
  function onSuccess(data){
  }

  function onFailure(error){
    if(error == "InvalidResetToken"){
      displayMessage("Invalid Reset Token");
    }
    $(".error-message").html(status);
    window.location.href='/knowledge/login';

  }
  mirror.validateResetToken("a7da78729ce049d8b29f2520c8c57496", 
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
  }
);
});