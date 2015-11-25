function saveRecord () { 
    $("#error").text("");
    var username = $("#username").val();

    alert("username: "+username);
    
    if(username == '') {
      $("#error").text("User Name Required"); 
    } else {
        function success(status,data) {
          if(status == 'success') {
            $("#error").text("Password Reset Link send to your Mail Id");
            $("#username").val("");
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.forgotPassword("ForgotPassword", username, success, failure);
      }
  }

  function resetPassword () { 
    $("#error").text("");
    var newpassword = $("#newpassword").val();
    var confirmpassword = $("#confirmpassword").val();

    alert("newpassword:" + newpassword);

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
        mirror.changePassword("ChangePassword", currentpassword, newpassword, success, failure);
      }
  }