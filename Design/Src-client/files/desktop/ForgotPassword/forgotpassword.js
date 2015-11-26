function saveRecord () { 
    $("#error").text("");
    var username = $("#username").val();
    
    if(username == '') {
      $("#error").text("User Name Required"); 
    } else {
        function success(status,data) {
          if(status == 'ForgotPasswordSuccess') {
            $("#error").text("Password Reset Link send to your Mail Id");
            $("#username").val("");
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.forgotPassword("AdminAPI", username, success, failure);
      }
  }
