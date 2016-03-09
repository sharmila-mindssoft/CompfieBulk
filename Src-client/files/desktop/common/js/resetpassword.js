function displayMessage(message) {
  console.log("inside displayMessage");
  console.log("obj:"+$(".error-message"))
  $(".error-message").html(message);
  $(".error-message").show();
}
$("#submit").click(function(){
    $(".error-message").html("");
    url = window.location.href;
    url_parameters = url.split("/");
    reset_token = url_parameters[url_parameters.length - 1];
    var resetToken = reset_token;

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
          if(error == "EnterDifferentPassword"){
            displayMessage("Password already used. Enter different password");
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
    // window.location.href='/knowledge/login';

  }
  url = window.location.href;
  url_parameters = url.split("/");
  reset_token = url_parameters[url_parameters.length - 1];
  mirror.validateResetToken(reset_token, 
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