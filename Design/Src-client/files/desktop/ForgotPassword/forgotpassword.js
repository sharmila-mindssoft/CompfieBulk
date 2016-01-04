$(".btn-domain-cancel").click(function(){
  window.location.href='/login';
});

$("#submit").click(function(){
    $(".error-message").html("");
    var username = $("#username").val();
    if(username == '') {
      $(".error-message").html("User Name Required"); 
    } else {
        function success(status,data) {
          if(status == 'ForgotPasswordSuccess') {
            $(".error-message").html("Password Reset Link send to your Mail Id");
            $("#username").val("");
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.forgotPassword("AdminAPI", username, success, failure);
      }
  });
