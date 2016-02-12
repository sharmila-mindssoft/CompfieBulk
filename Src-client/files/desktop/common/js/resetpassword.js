$("#submit").click(function(){
    $(".error-message").html("");
    var resetToken = "71546293895338817723334292533594853377";
    var newpassword = $("#newpassword").val();
    var confirmpassword = $("#confirmpassword").val();

    if(newpassword == '') {
      $(".error-message").html("New Password Required");
    } else if(confirmpassword == '') {
      $(".error-message").html("Confirm Password Required");
    } else if(confirmpassword != newpassword) {
      $(".error-message").html("New Password & Confirm Password is Not Match");
    } else {
        function success(status,data) {
          if(status == 'ResetPasswordSuccess') {
            $(".error-message").html("Password Changed Successfully");
            $("#newpassword").val("");
            $("#confirmpassword").val("");
          } else {
            $(".error-message").html(status);
          }
        }
        function failure(data){
        }
        mirror.resetPassword("AdminAPI", resetToken, newpassword, success, failure);
      }
  });

$(document).ready(function(){
  function success(status,data) {
  if(status == 'ResetTokenValidationSuccess') {
  
  }
  else {
    $(".error-message").html(status);
    window.location.href='/login';
  }
  }
  function failure(data){
  }
  mirror.validateResetToken("AdminAPI", "71546293895338817723334292533594853377", success, failure)
  });