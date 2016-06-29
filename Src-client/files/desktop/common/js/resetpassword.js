function displayMessage(message) {
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
      $(".error-message").html(message.npassword_required);
    } else if(confirmpassword.length == 0) {
      $(".error-message").html(message.conpassword_required);
    } else if(confirmpassword != newpassword) {
      $(".error-message").html(message.password_notmatch);
    } else {
      url = window.location.href;
      url_parameters = url.split("/");
      reset_token = url_parameters[url_parameters.length - 1];
      if(url_parameters[url_parameters.length - 2] != "reset-password"){
          function onSuccess(data){
          displayMessage(message.password_reset_success);
          $("#newpassword").val("");
          $("#confirmpassword").val("");
        }
        function onFailure(error){
          if(error == "InvalidResetToken"){
            displayMessage(message.invalid_reset_token);
          }
          if(error == "EnterDifferentPassword"){
            displayMessage(message.password_already_used);
          }
        }
        client_mirror.resetPassword(resetToken, newpassword,url_parameters[url_parameters.length - 2],
          function (error, response) {
            if (error == null){
              onSuccess(response);
            }
            else {
              onFailure(error);
            }
        }
        );
      }else{

        function onSuccess(data){
            displayMessage(message.password_reset_success);
            $("#newpassword").val("");
            $("#confirmpassword").val("");
          }
          function onFailure(error){
            if(error == "InvalidResetToken"){
              displayMessage(message.invalid_reset_token);
            }
            if(error == "EnterDifferentPassword"){
              displayMessage(message.password_already_used);
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
      }
  });

$(document).ready(function(){

  $('#newpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });
  $('#confirmpassword').keyup('input', function (event) {
      this.value = this.value.replace(/\s/g, '');
  });

  function onSuccess(data){
    // if (data[0] == "InvalidResetToken"){
    //   displayMessage("Invalid Reset Token");
    //   $(".error-message").html(status);
    // }

  }

  function onFailure(error){
    $(".error-message").html("Invalid Reset Token");
    $(".error-message").show();
  }
  url = window.location.href;
  url_parameters = url.split("/");
  reset_token = url_parameters[url_parameters.length - 1];
  if(url_parameters[url_parameters.length - 2] != "reset-password"){
       client_mirror.validateResetToken(reset_token, url_parameters[url_parameters.length - 2],
          function (error, response) {
            if (error == null){
              onSuccess(response);
            }
            else {
              onFailure(error);
            }
        }
      );
  }else{

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
  }

});