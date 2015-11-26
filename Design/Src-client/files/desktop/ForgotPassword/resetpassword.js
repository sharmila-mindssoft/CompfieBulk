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
  mirror.validateResetToken("AdminAPI", "314341777276858582911697971726622782117", success, failure)
  });

function resetPassword () { 
    $("#error").text("");
    var resetToken = "314341777276858582911697971726622782117";
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
          if(status == 'success') {
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