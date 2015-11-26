function saveRecord () { 

    $("#error").text("");
    var currentpassword = $("#currentpassword").val();
    var newpassword = $("#newpassword").val();
    var confirmpassword = $("#confirmpassword").val();

    alert("currentpassword:" + currentpassword);
    alert("newpassword:" + newpassword);

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
          if(status == 'success') {
            $("#error").text("Password Changed Successfully");
            $("#currentpassword").val("");
            $("#newpassword").val("");
            $("#confirmpassword").val("");
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.changePassword("AdminAPI", currentpassword, newpassword, success, failure);
      }
  }