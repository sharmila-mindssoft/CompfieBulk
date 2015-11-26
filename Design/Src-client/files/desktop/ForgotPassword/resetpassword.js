$(document).ready(function(){

  function success(status,data) {
  if(status == 'ResetTokenValidationSuccess') {
  
  } else {
    $("#error").text(status);
    window.location.href='/login';
  }
  }
  function failure(data){
  }
  mirror.validateResetToken("AdminAPI", "b4c59894336c4ee3b598f5e4bd2b276b", success, failure)
  });

function resetPassword () { 
    $("#error").text("");
    var resetToken = "b4c59894336c4ee3b598f5e4bd2b276b";
    var newpassword = $("#newpassword").val();
    var confirmpassword = $("#confirmpassword").val();

    if(newpassword == '') {
      $("#error").text("New Password Required");
    } else if(confirmpassword == '') {
      $("#error").text("Confirm Password Required");
    } else if(confirmpassword != newpassword) {
      $("#error").text("New Password & Confirm Password is Not Match");
    } else {
        function success(status,data) {
          if(status == 'ResetPasswordSuccess') {
            $("#error").text("Password Changed Successfully");
            $("#newpassword").val("");
            $("#confirmpassword").val("");
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.resetPassword("AdminAPI", resetToken, newpassword, success, failure);
      }
  }