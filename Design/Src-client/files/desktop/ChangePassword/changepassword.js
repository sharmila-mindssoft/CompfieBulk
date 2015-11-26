function saveRecord () { 

    $("#error").text("");
    var currentpassword = $("#currentpassword").val();
    var newpassword = $("#newpassword").val();
    var confirmpassword = $("#confirmpassword").val();

    if(currentpassword == '') {
      $("#error").text("Current Password Required");
    } else if(newpassword == '') {
      $("#error").text("New Password Required");
    } else if(confirmpassword == '') {
      $("#error").text("Confirm Password Required");
    } else if(confirmpassword != newpassword) {
      $("#error").text("New Password & Confirm Password is Not Match");
    } else {
        function success(status,data) {
          if(status == 'ChangePasswordSuccess') {
            $("#error").text("Password Changed Successfully");
            $("#currentpassword").val("");
            $("#newpassword").val("");
            $("#confirmpassword").val("");
            //window.location.href='/login';
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.changePassword("AdminAPI", currentpassword, newpassword, success, failure);
      }
  }