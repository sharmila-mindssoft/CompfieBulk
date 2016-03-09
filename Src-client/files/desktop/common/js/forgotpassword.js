function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$(".btn-forgotpassword-cancel").click(function(){
  var pathArray = window.location.pathname.split( '/' );
  if (pathArray[1] === 'knowledge'){
    window.location.href='/knowledge/login';
  }else{
    window.location.href='/login/';
  }
  
});

$("#submit").click(function(){
    displayMessage("");
    var username = $("#username").val().trim();
    if(username.length == 0) {
      displayMessage("Username required");
    } else {

        function onSuccess(data){
          displayMessage("Password reset link has been sent to your email Id");
          $("#username").val("");
        }
        function onFailure(error){
          if(error == "InvalidUserName"){
            displayMessage("No such user exists");
          }
        }
        mirror.forgotPassword(username, 
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
