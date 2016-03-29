function displayMessage(message) {
  console.log("inside displayMessage");
  console.log("obj:"+$(".error-message"))
  $(".error-message").html(message);
  $(".error-message").show();
}
$("#submit").click(function(){
    console.log("inside submit");
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
      $(".error-message").html("New Password & Confirm Password Do Not Match");
    } else {
      url = window.location.href;
      url_parameters = url.split("/");
      console.log(url_parameters);
      reset_token = url_parameters[url_parameters.length - 1];
      if(url_parameters[url_parameters.length - 2] != "reset-password"){
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
    console.log("inside onSuccess" + data);
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
  console.log(url_parameters);
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