$("#submit").click(function(){
  $(".error-message").html("");
  var currentpassword = $("#currentpassword").val();
  var newpassword = $("#newpassword").val();
  var confirmpassword = $("#confirmpassword").val();
  if(currentpassword == '') {
    $(".error-message").html("Current Password Required");
  } else if(newpassword == '') {
    $(".error-message").html("New Password Required");
  } else if(confirmpassword == '') {
    $(".error-message").html("Confirm Password Required");
  } else if(confirmpassword != newpassword) {
    $(".error-message").html("New Password & Confirm Password is Not Match");
  } else {
      function success(status,data) {
        if(status == 'ChangePasswordSuccess') {
          $(".error-message").html("Password Changed Successfully");
          $("#currentpassword").val("");
          $("#newpassword").val("");
          $("#confirmpassword").val("");
        } else {
          $(".error-message").html(status);
        }
      }
      function failure(data){
      }
      mirror.changePassword("AdminAPI", currentpassword, newpassword, success, failure);
    }
  });